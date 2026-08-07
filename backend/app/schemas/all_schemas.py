from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.all_models import RoleEnum, MedicineTypeEnum, FoodRelationEnum, DoseSlotEnum, DoseStatusEnum, ReportCategoryEnum, VaccineStatusEnum

# Token Schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    role: str

# Auth & User Schemas
class UserRegisterSchema(BaseModel):
    full_name: str
    age: int
    gender: str
    blood_group: str
    mobile_number: str
    email: EmailStr
    password: str
    address: Optional[str] = ""
    emergency_contact_number: Optional[str] = ""
    role: RoleEnum = RoleEnum.PATIENT

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    full_name: str
    age: int
    gender: str
    blood_group: str
    mobile_number: str
    email: str
    role: str
    is_verified: bool

    class Config:
        from_attributes = True

# Medicine Schemas
class ScheduleCreateSchema(BaseModel):
    dose_slot: DoseSlotEnum
    scheduled_time: str
    dosage_quantity: str

class MedicineCreateSchema(BaseModel):
    medicine_name: str
    photo_url: Optional[str] = ""
    medicine_type: MedicineTypeEnum
    food_relation: FoodRelationEnum
    start_date: str
    end_date: str
    repeat_pattern: Optional[str] = "DAILY"
    notes: Optional[str] = ""
    schedules: List[ScheduleCreateSchema]

class DoseStatusUpdateSchema(BaseModel):
    schedule_id: str
    status: DoseStatusEnum

# Medical Report Schema
class ReportCreateSchema(BaseModel):
    title: str
    category: ReportCategoryEnum
    hospital_name: str
    doctor_name: str
    report_date: str
    description: Optional[str] = ""
    file_type: str = "PDF"

# Doctor Permission Schema
class AccessRequestSchema(BaseModel):
    patient_mobile_or_id: str

class AccessApproveSchema(BaseModel):
    duration_hours: int = 24

# Vaccine Schema
class VaccineCreateSchema(BaseModel):
    vaccine_name: str
    scheduled_date: str
    doctor_or_clinic: Optional[str] = ""
    notes: Optional[str] = ""
