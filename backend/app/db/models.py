import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum, DateTime, Text, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

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

class StatusEnum(str, enum.Enum):
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

class ApprovalStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AccessStatusEnum(str, enum.Enum):
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

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    mobile_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    address = Column(String, nullable=True)
    emergency_contact_number = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.PATIENT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    medical_license_number = Column(String, unique=True, nullable=False)
    specialization = Column(String, nullable=False)
    hospital_affiliation = Column(String, nullable=True)
    is_identity_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="doctor_profile")

class Medicine(Base):
    __tablename__ = "medicines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    medicine_name = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    medicine_type = Column(Enum(MedicineTypeEnum), nullable=False)
    food_relation = Column(Enum(FoodRelationEnum), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    repeat_pattern = Column(Enum(RepeatPatternEnum), nullable=False)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    schedules = relationship("MedicineSchedule", back_populates="medicine")

class MedicineSchedule(Base):
    __tablename__ = "medicine_schedules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medicine_id = Column(UUID(as_uuid=True), ForeignKey("medicines.id"))
    dose_slot = Column(Enum(DoseSlotEnum), nullable=False)
    scheduled_time = Column(Time, nullable=False)
    dosage_quantity = Column(String, nullable=False)

    medicine = relationship("Medicine", back_populates="schedules")
    history = relationship("MedicineHistory", back_populates="schedule")

class MedicineHistory(Base):
    __tablename__ = "medicine_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("medicine_schedules.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(Time, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    action_timestamp = Column(DateTime, nullable=True)

    schedule = relationship("MedicineSchedule", back_populates="history")

class MedicalReport(Base):
    __tablename__ = "medical_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    category = Column(Enum(ReportCategoryEnum), nullable=False)
    hospital_name = Column(String, nullable=True)
    doctor_name = Column(String, nullable=True)
    report_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # PDF or IMAGE
    encryption_key_alias = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Vaccination(Base):
    __tablename__ = "vaccinations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    vaccine_name = Column(String, nullable=False)
    scheduled_date = Column(Date, nullable=True)
    administered_date = Column(Date, nullable=True)
    status = Column(Enum(VaccineStatusEnum), nullable=False)
    doctor_or_clinic = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    contact_name = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

class Caregiver(Base):
    __tablename__ = "caregivers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Enum(ApprovalStatusEnum), default=ApprovalStatusEnum.PENDING)
    receive_missed_dose_alert = Column(Boolean, default=False)
    receive_emergency_alert = Column(Boolean, default=False)
    receive_vaccine_alert = Column(Boolean, default=False)

class AccessPermission(Base):
    __tablename__ = "access_permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    status = Column(Enum(AccessStatusEnum), default=AccessStatusEnum.PENDING)
    requested_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    scope_permissions = Column(String, nullable=True)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    type = Column(Enum(NotificationTypeEnum), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
