from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.all_models import Vaccination
from app.schemas.all_schemas import VaccineCreateSchema
from app.core.security import get_current_user

router = APIRouter(prefix="/vaccines", tags=["VaccineService"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def log_vaccination(
    vax_in: VaccineCreateSchema,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_vax = Vaccination(
        user_id=current_user.user_id,
        vaccine_name=vax_in.vaccine_name,
        scheduled_date=vax_in.scheduled_date,
        doctor_or_clinic=vax_in.doctor_or_clinic,
        notes=vax_in.notes
    )
    db.add(new_vax)
    await db.commit()
    await db.refresh(new_vax)
    return new_vax

@router.get("")
async def get_patient_vaccines(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Vaccination).where(Vaccination.user_id == current_user.user_id))
    vaccines = result.scalars().all()
    return vaccines
