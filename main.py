from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import your DB setup and models
from .database import Base, engine, SessionLocal, Guest


# Create FastAPI instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://samuelandmakenna.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (optional, but handy for small projects)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for RSVP status
class RSVPResponse(BaseModel):
    status: str  # e.g. "joyfully accepts" or "regrettfully declines"

# GET endpoint to search for guests by name
@app.get("/rsvp")
def search_guest(
    name: str = Query(..., description="Name to search for in the guest list"),
    db: Session = Depends(get_db)
):
    # Case-insensitive search using ilike (PostgreSQL)
    results = db.query(Guest).filter(Guest.name.ilike(f"%{name}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail="Guest not found")
    return results

# POST endpoint to update the RSVP status for a specific guest
@app.post("/rsvp/{guest_id}")
def update_rsvp(
    guest_id: int,
    response: RSVPResponse,
    db: Session = Depends(get_db)
):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    guest.status = response.status
    db.commit()
    db.refresh(guest)

    return {"message": "RSVP updated", "guest": guest}
