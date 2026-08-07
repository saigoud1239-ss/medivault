from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import date, datetime
from app.db.models import ReportCategoryEnum

class MedicalReportBase(BaseModel):
    title: str
    category: ReportCategoryEnum
    hospital_name: Optional[str] = None
    doctor_name: Optional[str] = None
    report_date: date
    description: Optional[str] = None

class MedicalReportCreate(MedicalReportBase):
    pass

class MedicalReportResponse(MedicalReportBase):
    id: UUID4
    user_id: UUID4
    file_url: str
    file_type: str
    encryption_key_alias: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
