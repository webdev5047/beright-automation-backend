import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbx1bninRIrzhCcpvODLN1AgzIBN2zgzPedztZ2vCicOessHFsn0gmK0ANS0hRCJ85SP/exec"

@app.post("/webhook/lead-capture")
async def receive_webhook(request: Request):
    payload = await request.json()
    print("🔔 Webhook Event Received on Render Cloud!")
    print(json.dumps(payload, indent=2))

    try:
        requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload)
        print("✅ Synced to Google Sheets successfully!")
    except Exception as e:
        print(f"❌ Error syncing to sheet: {e}")

    return {
        "status": "success",
        "message": "Data processed on Render Cloud!",
        "received_data": payload
    }

if __name__ == "__main__":
    # Render provides a dynamic port; fallback to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("webhook_listener:app", host="0.0.0.0", port=port)