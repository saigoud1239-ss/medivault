import os
from celery import Celery
from app.core.config import settings
from datetime import timedelta

# Initialize Celery
celery_app = Celery(
    "medivault_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # In a real app we might route tasks to specific queues
    task_routes={
        "app.tasks.missed_dose_escalation.*": {"queue": "high_priority"},
    }
)

@celery_app.task
def check_missed_dose(schedule_id: str, user_id: str):
    """
    Background job triggered 30 mins after a scheduled dose.
    If the dose is not marked as TAKEN, we escalate to caregivers.
    """
    # Note: Inside Celery workers, we'd use sync SQLAlchemy or asyncio loop to query DB
    # For now, we simulate the logic.
    print(f"Checking missed dose for schedule {schedule_id} of user {user_id}")
    # In full implementation:
    # 1. Query MedicineHistory for this schedule_id and today's date
    # 2. If status != TAKEN:
    # 3.    Update status to MISSED
    # 4.    Fetch Caregivers linked to user_id where receive_missed_dose_alert=True
    # 5.    Dispatch FCM/Twilio alerts to caregivers
    
    return {"status": "checked", "schedule_id": schedule_id}
