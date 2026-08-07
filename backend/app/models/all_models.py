import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base

# Enums
class RoleEnum(str, enum.Enum):
    PATIENT = "PATIENT"
    CAREGIVER = "CAREGIVER"
    ADMIN = "ADMIN"

class MedicineTypeEnum(str, enum.Enum):
    TABLET = "TABLET"
    CAPSULE = "CAPSULE"
    SYRUP = "SYRUP"
    INJECTION = "INJECTION"

class FoodRelationEnum(str, enum.Enum):
    BEFORE_FOOD = "BEFORE_FOOD"
    AFTER_FOOD = "AFTER_FOOD"

class RepeatPatternEnum(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class DoseSlotEnum(str, enum.Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"
    NIGHT = "NIGHT"
    CUSTOM = "CUSTOM"

class DoseStatusEnum(str, enum.Enum):
    TAKEN = "TAKEN"
    SNOOZED = "SNOOZED"
    SKIPPED = "SKIPPED"
    MISSED = "MISSED"

class ReportCategoryEnum(str, enum.Enum):
    PRESCRIPTION = "PRESCRIPTION"
    BLOOD_REPORT = "BLOOD_REPORT"
    XRAY = "XRAY"
    MRI = "MRI"
    CT_SCAN = "CT_SCAN"
    OPERATION_REPORT = "OPERATION_REPORT"
    DISCHARGE_SUMMARY = "DISCHARGE_SUMMARY"
    LAB_REPORT = "LAB_REPORT"
    DOCTOR_NOTES = "DOCTOR_NOTES"
    DISEASE_HISTORY = "DISEASE_HISTORY"
    SURGERY_HISTORY = "SURGERY_HISTORY"

class VaccineStatusEnum(str, enum.Enum):
    COMPLETED = "COMPLETED"
    UPCOMING = "UPCOMING"
    MISSED = "MISSED"

class CaregiverStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class PermissionStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"

class NotificationTypeEnum(str, enum.Enum):
    MEDICATION = "MEDICATION"
    EMERGENCY = "EMERGENCY"
    DOCTOR_REQUEST = "DOCTOR_REQUEST"
    VACCINATION = "VACCINATION"
    CAREGIVER = "CAREGIVER"


# 1. Users Table
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    blood_group: Mapped[str] = mapped_column(String(10), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    emergency_contact_number: Mapped[str] = mapped_column(String(50), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum), default=RoleEnum.PATIENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 2. Doctors Table
class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    medical_license_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    hospital_affiliation: Mapped[str] = mapped_column(String(255), nullable=False)
    is_identity_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# 3. Medicines Table
class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    medicine_name: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    medicine_type: Mapped[MedicineTypeEnum] = mapped_column(SQLEnum(MedicineTypeEnum), nullable=False)
    food_relation: Mapped[FoodRelationEnum] = mapped_column(SQLEnum(FoodRelationEnum), nullable=False)
    start_date: Mapped[str] = mapped_column(String(50), nullable=False)
    end_date: Mapped[str] = mapped_column(String(50), nullable=False)
    repeat_pattern: Mapped[RepeatPatternEnum] = mapped_column(SQLEnum(RepeatPatternEnum), default=RepeatPatternEnum.DAILY)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# 4. MedicineSchedules Table
class MedicineSchedule(Base):
    __tablename__ = "medicine_schedules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    medicine_id: Mapped[str] = mapped_column(String(36), ForeignKey("medicines.id"), nullable=False)
    dose_slot: Mapped[DoseSlotEnum] = mapped_column(SQLEnum(DoseSlotEnum), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(String(50), nullable=False)
    dosage_quantity: Mapped[str] = mapped_column(String(50), nullable=False)


# 5. MedicineHistory Table
class MedicineHistory(Base):
    __tablename__ = "medicine_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id: Mapped[str] = mapped_column(String(36), ForeignKey("medicine_schedules.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    scheduled_date: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[DoseStatusEnum] = mapped_column(SQLEnum(DoseStatusEnum), nullable=False)
    action_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# 6. MedicalReports Table
class MedicalReport(Base):
    __tablename__ = "medical_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[ReportCategoryEnum] = mapped_column(SQLEnum(ReportCategoryEnum), nullable=False)
    hospital_name: Mapped[str] = mapped_column(String(255), nullable=False)
    doctor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    report_date: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    encryption_key_alias: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# 7. Vaccinations Table
class Vaccination(Base):
    __tablename__ = "vaccinations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    vaccine_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_date: Mapped[str] = mapped_column(String(50), nullable=False)
    administered_date: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[VaccineStatusEnum] = mapped_column(SQLEnum(VaccineStatusEnum), default=VaccineStatusEnum.UPCOMING)
    doctor_or_clinic: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)


# 8. EmergencyContacts Table
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)


# 9. Caregivers Table
class Caregiver(Base):
    __tablename__ = "caregivers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    caregiver_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    status: Mapped[CaregiverStatusEnum] = mapped_column(SQLEnum(CaregiverStatusEnum), default=CaregiverStatusEnum.PENDING)
    receive_missed_dose_alert: Mapped[bool] = mapped_column(Boolean, default=True)
    receive_emergency_alert: Mapped[bool] = mapped_column(Boolean, default=True)
    receive_vaccine_alert: Mapped[bool] = mapped_column(Boolean, default=True)


# 10. AccessPermissions Table
class AccessPermission(Base):
    __tablename__ = "access_permissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    doctor_id: Mapped[str] = mapped_column(String(36), ForeignKey("doctors.id"), nullable=False)
    status: Mapped[PermissionStatusEnum] = mapped_column(SQLEnum(PermissionStatusEnum), default=PermissionStatusEnum.PENDING)
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    scope_permissions: Mapped[str] = mapped_column(Text, default="READ_REPORTS,READ_PRESCRIPTIONS")


# 11. Notifications Table
class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationTypeEnum] = mapped_column(SQLEnum(NotificationTypeEnum), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
