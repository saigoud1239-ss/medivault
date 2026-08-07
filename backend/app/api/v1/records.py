from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date
import uuid
import os

from app.api.deps import get_db, require_role
from app.db.models import User, MedicalReport, ReportCategoryEnum, RoleEnum
from app.schemas.records import MedicalReportResponse

router = APIRouter()

@router.post("/upload", response_model=MedicalReportResponse, status_code=status.HTTP_201_CREATED)
async def upload_medical_report(
    title: str = Form(...),
    category: ReportCategoryEnum = Form(...),
    report_date: date = Form(...),
    hospital_name: str = Form(None),
    doctor_name: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    """
    Upload a medical report.
    Implements mock Envelope Encryption (DEK/KEK) and mock S3 storage.
    """
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_type = "PDF" if file_ext == ".pdf" else "IMAGE"
    
    # --- MOCK ENVELOPE ENCRYPTION ---
    # 1. Generate a unique Data Encryption Key (DEK)
    mock_dek = os.urandom(32) 
    
    # 2. Encrypt the file content with the DEK (AES-256 GCM)
    # mock_encrypted_content = aes_gcm_encrypt(file.read(), mock_dek)
    
    # 3. Encrypt the DEK with a Key Encryption Key (KEK) from AWS KMS
    # mock_encrypted_dek = aws_kms.encrypt(mock_dek, key_id="arn:aws:kms:...")
    
    # 4. Upload encrypted content to S3
    mock_s3_url = f"s3://{current_user.id}/{uuid.uuid4()}{file_ext}"
    
    # 5. Store the encrypted DEK alongside the metadata or in a secure vault
    mock_key_alias = f"kms-alias-{uuid.uuid4()}"

    # Create Database Record
    report = MedicalReport(
        user_id=current_user.id,
        title=title,
        category=category,
        hospital_name=hospital_name,
        doctor_name=doctor_name,
        report_date=report_date,
        description=description,
        file_url=mock_s3_url,
        file_type=file_type,
        encryption_key_alias=mock_key_alias
    )
    
    db.add(report)
    await db.commit()
    await db.refresh(report)
    
    # In a full implementation, trigger an async Celery task here to run OCR via Cloud Vision
    
    return report

@router.get("/", response_model=list[MedicalReportResponse])
async def list_medical_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.PATIENT]))
):
    """List all medical reports for the current patient"""
    result = await db.execute(
        select(MedicalReport).filter(MedicalReport.user_id == current_user.id)
    )
    return result.scalars().all()
