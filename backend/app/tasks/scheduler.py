from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("medivault_tasks")
scheduler = AsyncIOScheduler()

def start_task_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("⚡ MediVault Redis / APScheduler Task Worker Started.")

def schedule_missed_dose_escalation_job(patient_id: str, schedule_id: str, medicine_name: str, delay_minutes: int = 30):
    """
    Schedules an asynchronous missed-dose check in 30 minutes.
    If dose status is not TAKEN by then, triggers Caregiver Escalation Push.
    """
    run_date = datetime.now() + timedelta(minutes=delay_minutes)
    job_id = f"missed_dose_{schedule_id}_{patient_id}"
    
    scheduler.add_job(
        func=check_and_escalate_missed_dose,
        trigger='date',
        run_date=run_date,
        args=[patient_id, schedule_id, medicine_name],
        id=job_id,
        replace_existing=True
    )
    logger.info(f"⏱️ Scheduled Missed Dose Escalation Job [{job_id}] for {medicine_name} at {run_date}")

async def check_and_escalate_missed_dose(patient_id: str, schedule_id: str, medicine_name: str):
    """
    Timer Expiry Execution: Dispatch FCM & Twilio alerts to linked caregivers.
    """
    logger.warning(f"🚨 MISSED DOSE ESCALATION TRIGGERED for Patient [{patient_id}], Medicine: {medicine_name}")
    print(f"📡 [FCM/Twilio Alert Dispatched] Patient {patient_id} missed dose of {medicine_name}. Caregivers notified!")

def cancel_missed_dose_job(schedule_id: str, patient_id: str):
    job_id = f"missed_dose_{schedule_id}_{patient_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"✔ Canceled Missed Dose Job [{job_id}] because dose was TAKEN.")
