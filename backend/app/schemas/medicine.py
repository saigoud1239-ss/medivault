from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import date, time, datetime
from app.db.models import MedicineTypeEnum, FoodRelationEnum, RepeatPatternEnum, DoseSlotEnum, StatusEnum

class MedicineScheduleBase(BaseModel):
    dose_slot: DoseSlotEnum
    scheduled_time: time
    dosage_quantity: str

class MedicineScheduleCreate(MedicineScheduleBase):
    pass

class MedicineScheduleResponse(MedicineScheduleBase):
    id: UUID4
    medicine_id: UUID4

    class Config:
        from_attributes = True

class MedicineBase(BaseModel):
    medicine_name: str
    photo_url: Optional[str] = None
    medicine_type: MedicineTypeEnum
    food_relation: FoodRelationEnum
    start_date: date
    end_date: Optional[date] = None
    repeat_pattern: RepeatPatternEnum
    notes: Optional[str] = None

class MedicineCreate(MedicineBase):
    schedules: List[MedicineScheduleCreate]

class MedicineResponse(MedicineBase):
    id: UUID4
    user_id: UUID4
    is_active: bool
    created_at: datetime
    schedules: List[MedicineScheduleResponse] = []

    class Config:
        from_attributes = True

class MedicineHistoryLogBase(BaseModel):
    schedule_id: UUID4
    scheduled_date: date
    scheduled_time: time
    status: StatusEnum

class MedicineHistoryLogCreate(MedicineHistoryLogBase):
    pass

class MedicineHistoryLogResponse(MedicineHistoryLogBase):
    id: UUID4
    user_id: UUID4
    action_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
