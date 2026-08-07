from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, medicines, emergency, doctor_consent, records

app = FastAPI(
    title="MediVault API",
    description="Cross-platform healthcare management app API",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(medicines.router, prefix="/api/v1/medicines", tags=["medicines"])
app.include_router(emergency.router, prefix="/api/v1/emergency", tags=["emergency"])
app.include_router(doctor_consent.router, prefix="/api/v1/doctors", tags=["doctors"])
app.include_router(records.router, prefix="/api/v1/records", tags=["records"])

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to MediVault API"}
