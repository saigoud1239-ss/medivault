from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import uuid
from datetime import datetime

from app.api.deps import get_db, get_current_active_user, require_role
from app.db.models import Medicine, MedicineSchedule, MedicineHistory, User, RoleEnum, StatusEnum
from app.schemas.medicine import MedicineCreate, MedicineResponse, MedicineHistoryLogCreate, MedicineHistoryLogResponse

router = APIRouter()

@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
async def create_medicine(
    medicine_in: MedicineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    # Create Medicine
    medicine = Medicine(
        user_id=current_user.id,
        medicine_name=medicine_in.medicine_name,
        photo_url=medicine_in.photo_url,
        medicine_type=medicine_in.medicine_type,
        food_relation=medicine_in.food_relation,
        start_date=medicine_in.start_date,
        end_date=medicine_in.end_date,
        repeat_pattern=medicine_in.repeat_pattern,
        notes=medicine_in.notes
    )
    db.add(medicine)
    await db.flush() # To get medicine.id

    # Create Schedules
    for schedule_in in medicine_in.schedules:
        schedule = MedicineSchedule(
            medicine_id=medicine.id,
            dose_slot=schedule_in.dose_slot,
            scheduled_time=schedule_in.scheduled_time,
            dosage_quantity=schedule_in.dosage_quantity
        )
        db.add(schedule)
    
    await db.commit()
    
    # Fetch with relationships to return complete response
    result = await db.execute(
        select(Medicine).options(selectinload(Medicine.schedules)).filter(Medicine.id == medicine.id)
    )
    return result.scalar_one()

@router.get("/", response_model=List[MedicineResponse])
async def read_medicines(
    skip: int = 0, limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    result = await db.execute(
        select(Medicine)
        .options(selectinload(Medicine.schedules))
        .filter(Medicine.user_id == current_user.id)
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/log", response_model=MedicineHistoryLogResponse, status_code=status.HTTP_201_CREATED)
async def log_medicine_dose(
    log_in: MedicineHistoryLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    # Verify schedule belongs to current user's medicine
    result = await db.execute(
        select(MedicineSchedule).join(Medicine).filter(
            MedicineSchedule.id == log_in.schedule_id,
            Medicine.user_id == current_user.id
        )
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found or not owned by user")

    history_log = MedicineHistory(
        schedule_id=log_in.schedule_id,
        user_id=current_user.id,
        scheduled_date=log_in.scheduled_date,
        scheduled_time=log_in.scheduled_time,
        status=log_in.status,
        action_timestamp=datetime.utcnow() if log_in.status == StatusEnum.TAKEN else None
    )
    
    db.add(history_log)
    await db.commit()
    await db.refresh(history_log)
    
    # If the log is TAKEN, we would cancel the Redis escalation timer here
    # (Task to be implemented in Celery)
    
    return history_log
