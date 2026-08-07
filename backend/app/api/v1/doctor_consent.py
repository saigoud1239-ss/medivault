from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import uuid

from app.api.deps import get_db, require_role
from app.db.models import User, AccessPermission, AccessStatusEnum, RoleEnum
from app.schemas.doctor_consent import AccessPermissionResponse, ApproveAccessRequest

router = APIRouter()

@router.post("/request-access", response_model=AccessPermissionResponse)
async def request_access(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_doctor: User = Depends(require_role([RoleEnum.ADMIN])) # Mocking DOCTOR role as admin for now if Doctor is an extended model
):
    """
    Doctor requests access to patient records.
    Sets status to PENDING.
    """
    # Verify patient exists
    patient = await db.execute(select(User).filter(User.id == patient_id, User.role == RoleEnum.PATIENT))
    if not patient.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Patient not found")
        
    permission = AccessPermission(
        patient_id=patient_id,
        doctor_id=current_doctor.id,  # Assuming current_user is linked to a doctor
        status=AccessStatusEnum.PENDING,
        requested_at=datetime.utcnow()
    )
    
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    
    # In a full app, trigger FCM Push to patient here
    
    return permission

@router.put("/{permission_id}/approve", response_model=AccessPermissionResponse)
async def approve_access(
    permission_id: uuid.UUID,
    request: ApproveAccessRequest,
    db: AsyncSession = Depends(get_db),
    current_patient: User = Depends(require_role([RoleEnum.PATIENT]))
):
    """
    Patient approves doctor's access request for a chosen duration.
    """
    result = await db.execute(
        select(AccessPermission).filter(
            AccessPermission.id == permission_id,
            AccessPermission.patient_id == current_patient.id
        )
    )
    permission = result.scalar_one_or_none()
    if not permission:
        raise HTTPException(status_code=404, detail="Access request not found")
        
    permission.status = AccessStatusEnum.APPROVED
    permission.approved_at = datetime.utcnow()
    permission.expires_at = datetime.utcnow() + timedelta(days=request.duration_days)
    
    await db.commit()
    await db.refresh(permission)
    return permission

@router.get("/patient-records/{patient_id}")
async def get_patient_records(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_doctor: User = Depends(require_role([RoleEnum.ADMIN])) # Mock doctor role
):
    """
    Doctor views patient records. Must have an APPROVED and unexpired grant.
    """
    result = await db.execute(
        select(AccessPermission).filter(
            AccessPermission.patient_id == patient_id,
            AccessPermission.doctor_id == current_doctor.id,
            AccessPermission.status == AccessStatusEnum.APPROVED
        )
    )
    permission = result.scalar_one_or_none()
    
    if not permission or (permission.expires_at and permission.expires_at < datetime.utcnow()):
        raise HTTPException(status_code=403, detail="Access expired or not granted")
        
    # Would return actual patient records here (medicines, reports, etc.)
    return {"message": "Access granted", "patient_id": patient_id, "data": "Patient records"}
