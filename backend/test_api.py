"""End-to-end API test script for MediVault backend"""
import requests
import json
import sys

BASE = "http://127.0.0.1:8000/api/v1"

def test(name, method, url, **kwargs):
    try:
        r = getattr(requests, method)(url, **kwargs, timeout=5)
        status = r.status_code
        try:
            body = r.json()
        except:
            body = r.text[:200]
        ok = "PASS" if status < 400 else "FAIL"
        print(f"[{ok}] {name} -> {status}: {json.dumps(body, indent=2, default=str)[:300]}")
        return r
    except Exception as e:
        print(f"[FAIL] {name} -> Exception: {e}")
        return None

# 1. Health check
test("Health", "get", f"{BASE}/health")

# 2. Signup
r = test("Signup", "post", f"{BASE}/auth/signup", json={
    "full_name": "Test Patient",
    "email": "testdebug@medivault.app",
    "mobile_number": "1112223333",
    "password": "password123"
})

# 3. Login  
r = test("Login", "post", f"{BASE}/auth/login", data={
    "username": "testdebug@medivault.app",
    "password": "password123"
})

if r and r.status_code == 200:
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. Get /me
    test("Get Me", "get", f"{BASE}/auth/me", headers=headers)
    
    # 5. List medicines (should be empty)
    test("List Medicines", "get", f"{BASE}/medicines/", headers=headers)
    
    # 6. Create a medicine
    r = test("Create Medicine", "post", f"{BASE}/medicines/", headers=headers, json={
        "medicine_name": "Paracetamol 500mg",
        "medicine_type": "TABLET",
        "food_relation": "AFTER_FOOD",
        "start_date": "2026-08-08",
        "repeat_pattern": "DAILY",
        "schedules": [
            {"dose_slot": "MORNING", "scheduled_time": "08:00:00", "dosage_quantity": "1 tablet"},
            {"dose_slot": "NIGHT", "scheduled_time": "22:00:00", "dosage_quantity": "1 tablet"}
        ]
    })
    
    # 7. List medicines again (should have 1)
    test("List Medicines After Create", "get", f"{BASE}/medicines/", headers=headers)
    
    # 8. Log a dose
    if r and r.status_code == 201:
        med = r.json()
        if med.get("schedules"):
            sched_id = med["schedules"][0]["id"]
            test("Log Dose", "post", f"{BASE}/medicines/log", headers=headers, json={
                "schedule_id": sched_id,
                "scheduled_date": "2026-08-08",
                "scheduled_time": "08:00:00",
                "status": "TAKEN"
            })
else:
    print("[SKIP] No token — skipping authenticated tests")

print("\n--- DONE ---")
