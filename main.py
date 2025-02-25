from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import your DB setup and models
from database import Base, engine, SessionLocal, Guest


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
    db = SessionLocal()
    if db.query(Guest).count() == 0:
        db.add(Guest(name="Bartow Family", number_of_invitees=4))
        db.add(Guest(name="Warner Family", number_of_invitees=5))
        db.add(Guest(name="Grace", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Mack Family", number_of_invitees=3))
        db.add(Guest(name="Greg and Peg", number_of_invitees=2))
        db.add(Guest(name="Mckeithan Family", number_of_invitees=3))
        db.add(Guest(name="Jeddie", number_of_invitees=1))
        db.add(Guest(name="Smith Family", number_of_invitees=4))
        db.add(Guest(name="Farrell Family", number_of_invitees=3))
        db.add(Guest(name="Valeria", number_of_invitees=3))
        db.add(Guest(name="Hannah", number_of_invitees=2))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Lornezinis Family", number_of_invitees=5))
        db.add(Guest(name="Aya", number_of_invitees=1))
        db.add(Guest(name="India", number_of_invitees=1))
        db.add(Guest(name="Krywe Family", number_of_invitees=3))
        db.add(Guest(name="Dejong Family", number_of_invitees=6))
        db.add(Guest(name="Nicole", number_of_invitees=1))
        db.add(Guest(name="David", number_of_invitees=3))
        # If a guest has no explicit number in parentheses, assume 1 invitee:
        db.add(Guest(name="Andreu", number_of_invitees=1))
        db.add(Guest(name="Johnson Family", number_of_invitees=3))
        db.add(Guest(name="Grandpa Warner", number_of_invitees=1))
        db.add(Guest(name="Athey Family", number_of_invitees=4))
        db.add(Guest(name="Pop and Butter", number_of_invitees=2))
        db.add(Guest(name="Abuellie", number_of_invitees=1))
        db.add(Guest(name="Zach and Ellise", number_of_invitees=2))
        db.add(Guest(name="Oscar and Lily", number_of_invitees=2))
        db.add(Guest(name="Deneyi", number_of_invitees=3))
        db.add(Guest(name="Dayanna", number_of_invitees=2))
        db.add(Guest(name="Pepe and Jackie", number_of_invitees=2))
        db.add(Guest(name="Irma and Clemente", number_of_invitees=2))
        
        db.commit()
    db.close()


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
