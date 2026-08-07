from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import uuid

from app.api.deps import get_db, get_current_active_user, require_role
from app.db.models import User, EmergencyContact, RoleEnum
from app.schemas.emergency import EmergencyContactCreate, EmergencyContactResponse, EmergencyPublicView, QRCodeResponse

router = APIRouter()

@router.post("/contacts", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
async def add_emergency_contact(
    contact_in: EmergencyContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    contact = EmergencyContact(
        user_id=current_user.id,
        contact_name=contact_in.contact_name,
        relationship=contact_in.relationship,
        phone_number=contact_in.phone_number,
        is_primary=contact_in.is_primary
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

@router.get("/qr", response_model=QRCodeResponse)
async def generate_emergency_qr(
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    """
    Generates a signed, short-lived token URL for the Emergency QR.
    Mock implementation for the hackathon.
    """
    expires_at = datetime.utcnow() + timedelta(days=30)
    # In reality, this would be a signed JWT or similar in the URL
    qr_url = f"https://medivault.app/emergency/{current_user.id}?token=mock_signed_token_123"
    
    return QRCodeResponse(qr_url=qr_url, expires_at=expires_at)

@router.get("/public/{user_id}", response_model=EmergencyPublicView)
async def get_public_emergency_info(
    user_id: uuid.UUID,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Publicly accessible endpoint (no auth required), but expects a signed token.
    Resolves the public view.
    """
    if token != "mock_signed_token_123":
        raise HTTPException(status_code=403, detail="Invalid or expired emergency token")
        
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    contacts_result = await db.execute(select(EmergencyContact).filter(EmergencyContact.user_id == user_id))
    contacts = contacts_result.scalars().all()
    
    return EmergencyPublicView(
        user_id=user.id,
        full_name=user.full_name,
        blood_group=user.blood_group,
        emergency_contacts=contacts
    )
