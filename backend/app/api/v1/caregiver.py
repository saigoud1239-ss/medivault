from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.all_models import Caregiver, CaregiverStatusEnum
from app.core.security import get_current_user

router = APIRouter(prefix="/caregivers", tags=["CaregiverService"])

@router.get("")
async def get_patient_caregivers(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Caregiver).where(Caregiver.patient_id == current_user.user_id))
    caregivers = result.scalars().all()
    return caregivers
