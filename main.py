from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for your WordPress site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://samuelandmakenna.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated in-memory database of guests
guests = [
    {"id": 1, "name": "Warner Family", "number of invitees": 5, "status": None},
    {"id": 2, "name": "Bartow Family", "number of invitees": 4, "status": None},
    {"id": 3, "name": "Grace", "number of invitees": 1, "status": None},
    {"id": 4, "name": "Irma", "number of invitees": 2, "status": None},
]

# Pydantic model to validate RSVP response payload
class RSVPResponse(BaseModel):
    status: str  # Expect values like "joyfully accepts" or "regrettfully declines"

# GET endpoint to search for guests by name
@app.get("/rsvp")
def search_guest(name: str = Query(..., description="Name to search for in the guest list")):
    results = [guest for guest in guests if name.lower() in guest["name"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="Guest not found")
    return results

# POST endpoint to update the RSVP status for a specific guest
@app.post("/rsvp/{guest_id}")
def update_rsvp(guest_id: int, response: RSVPResponse):
    for guest in guests:
        if guest["id"] == guest_id:
            guest["status"] = response.status
            return {"message": "RSVP updated", "guest": guest}
    raise HTTPException(status_code=404, detail="Guest not found")
