from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.all_models import Medicine, MedicineSchedule, MedicineHistory, DoseStatusEnum
from app.schemas.all_schemas import MedicineCreateSchema, DoseStatusUpdateSchema
from app.core.security import get_current_user, require_roles
from app.tasks.scheduler import schedule_missed_dose_escalation_job, cancel_missed_dose_job

router = APIRouter(prefix="/medications", tags=["MedService"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_medicine(
    med_in: MedicineCreateSchema,
    current_user=Depends(require_roles(["PATIENT", "ADMIN"])),
    db: AsyncSession = Depends(get_db)
):
    new_med = Medicine(
        user_id=current_user.user_id,
        medicine_name=med_in.medicine_name,
        photo_url=med_in.photo_url,
        medicine_type=med_in.medicine_type,
        food_relation=med_in.food_relation,
        start_date=med_in.start_date,
        end_date=med_in.end_date,
        repeat_pattern=med_in.repeat_pattern,
        notes=med_in.notes
    )
    db.add(new_med)
    await db.commit()
    await db.refresh(new_med)

    schedules_out = []
    for sched in med_in.schedules:
        new_sched = MedicineSchedule(
            medicine_id=new_med.id,
            dose_slot=sched.dose_slot,
            scheduled_time=sched.scheduled_time,
            dosage_quantity=sched.dosage_quantity
        )
        db.add(new_sched)
        await db.commit()
        await db.refresh(new_sched)
        schedules_out.append(new_sched)

        # Schedule missed dose timer for active dosage
        schedule_missed_dose_escalation_job(
            patient_id=current_user.user_id,
            schedule_id=new_sched.id,
            medicine_name=new_med.medicine_name,
            delay_minutes=30
        )

    return {"message": "Medicine and dosage schedules created successfully", "id": new_med.id}

@router.get("")
async def get_patient_medicines(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Medicine).where(Medicine.user_id == current_user.user_id))
    medicines = result.scalars().all()
    return medicines

@router.post("/status")
async def update_dose_status(
    status_in: DoseStatusUpdateSchema,
    current_user=Depends(require_roles(["PATIENT", "ADMIN"])),
    db: AsyncSession = Depends(get_db)
):
    log_entry = MedicineHistory(
        schedule_id=status_in.schedule_id,
        user_id=current_user.user_id,
        scheduled_date=str(MedicineHistory.action_timestamp),
        scheduled_time="08:00",
        status=status_in.status
    )
    db.add(log_entry)
    await db.commit()

    if status_in.status == DoseStatusEnum.TAKEN:
        cancel_missed_dose_job(status_in.schedule_id, current_user.user_id)

    return {"message": f"Dose status updated to {status_in.status.name}", "schedule_id": status_in.schedule_id}
