from typing import List, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime
from app.schemas.user import UserResponse

class EmergencyContactBase(BaseModel):
    contact_name: str
    relationship: str
    phone_number: str
    is_primary: bool = False

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContactResponse(EmergencyContactBase):
    id: UUID4
    user_id: UUID4

    class Config:
        from_attributes = True

class EmergencyPublicView(BaseModel):
    user_id: UUID4
    full_name: str
    blood_group: Optional[str]
    emergency_contacts: List[EmergencyContactResponse]

class QRCodeResponse(BaseModel):
    qr_url: str
    expires_at: datetime
