from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.db.session import engine, Base
from app.tasks.scheduler import start_task_scheduler

# Import Routers
from app.api.v1.auth import router as auth_router
from app.api.v1.medication import router as med_router
from app.api.v1.records import router as records_router
from app.api.v1.doctor_consent import router as doctor_router
from app.api.v1.emergency import router as emergency_router
from app.api.v1.caregiver import router as caregiver_router
from app.api.v1.vaccine import router as vaccine_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="MediVault — Unified Mobile Healthcare Management System Backend API"
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Auto-create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    start_task_scheduler()

# Register Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(med_router, prefix=settings.API_V1_STR)
app.include_router(records_router, prefix=settings.API_V1_STR)
app.include_router(doctor_router, prefix=settings.API_V1_STR)
app.include_router(emergency_router, prefix=settings.API_V1_STR)
app.include_router(caregiver_router, prefix=settings.API_V1_STR)
app.include_router(vaccine_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
