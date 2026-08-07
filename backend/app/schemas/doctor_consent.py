from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime
from app.db.models import AccessStatusEnum
from app.schemas.user import UserResponse

class AccessPermissionBase(BaseModel):
    doctor_id: UUID4
    scope_permissions: Optional[str] = None

class AccessPermissionCreate(AccessPermissionBase):
    pass

class AccessPermissionResponse(AccessPermissionBase):
    id: UUID4
    patient_id: UUID4
    status: AccessStatusEnum
    requested_at: datetime
    approved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApproveAccessRequest(BaseModel):
    duration_days: int = 7
