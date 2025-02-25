from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_

# Import your DB setup and models
from database import Base, engine, SessionLocal, Guest

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://samuelandmakenna.com", "https://www.samuelandmakenna.com"],
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
        db.add(Guest(name="Bartow Family", members="Jussely, Eben, Elijah, Amalia", number_of_invitees=4))
        db.add(Guest(name="Warner Family", members="Kai, Jason, Annika, Savanna, Sophia", number_of_invitees=5))
        db.add(Guest(name="Grace", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Karen", number_of_invitees=1))
        db.add(Guest(name="Mack Family", members="Ryhs, Naomi, Troy", number_of_invitees=3))
        db.add(Guest(name="Underwood Family", members="Jeddie, Greg, Peg", number_of_invitees=2))
        db.add(Guest(name="Mckeithan Family", members="Julie, Peyton, Megan", number_of_invitees=3))
        db.add(Guest(name="Smith Family", members="Sarah, Jason, Nico, Luca", number_of_invitees=4))
        db.add(Guest(name="Farrell Family", members="Olivia, Brian, Theo", number_of_invitees=3))
        db.add(Guest(name="Valeria", members="Valeria, Tere, Erick", number_of_invitees=3))
        db.add(Guest(name="Hannah", members="Jesus, Hannah", number_of_invitees=2))
        db.add(Guest(name="Elena", number_of_invitees=1))
        db.add(Guest(name="Lornezini Family", members="Kylie, Kenna, Nate, Aubrey, Conner, Caleb", number_of_invitees=6))
        db.add(Guest(name="Aya", number_of_invitees=1))
        db.add(Guest(name="India", number_of_invitees=1))
        db.add(Guest(name="Sofia", number_of_invitees=1))
        db.add(Guest(name="Krywe Family", members="April, Diane, Tom", number_of_invitees=3))
        db.add(Guest(name="Dejong Family", members="Mike, Christina, Lauren, Austen, Jacob, Evan", number_of_invitees=6))
        db.add(Guest(name="Nicole", number_of_invitees=1))
        db.add(Guest(name="David", number_of_invitees=3))
        db.add(Guest(name="Andreu", number_of_invitees=1))
        db.add(Guest(name="Johnson Family", members="Max, Liz, Glenn", number_of_invitees=3))
        db.add(Guest(name="Grandpa Warner", number_of_invitees=1))
        db.add(Guest(name="Athey Family", members="Lynn, Shane, Malia, Emiko", number_of_invitees=4))
        db.add(Guest(name="Pop and Butter", number_of_invitees=2))
        db.add(Guest(name="Abuellie", members="Ellen", number_of_invitees=1))
        db.add(Guest(name="Zach and Elise", members="Zach, Elise", number_of_invitees=2))
        db.add(Guest(name="Oscar and Lily", members="Oscar, Lily", number_of_invitees=2))
        db.add(Guest(name="Deneyi", number_of_invitees=3))
        db.add(Guest(name="Dayanna", number_of_invitees=2))
        db.add(Guest(name="Pepe and Jackie", members="Pepe, Jackie", number_of_invitees=2))
        db.add(Guest(name="Irma and Clemente", members="Irma, Clemente", number_of_invitees=2))
        
        db.commit()
    db.close()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for RSVP status (field name updated for consistency)
class RSVPResponse(BaseModel):
    status: str  # e.g. "joyfully accepts" or "regrettfully declines"
    confirmed_attendance: int  # number of people confirmed 

# GET endpoint to search for guests by name and members
@app.get("/rsvp")
def search_guest(
    name: str = Query(..., description="Name to search for in the guest list"),
    db: Session = Depends(get_db)
):
    results = db.query(Guest).filter(
        or_(
            Guest.name.ilike(f"%{name}%"),
            Guest.members.ilike(f"%{name}%")
        )
    ).all()
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
    guest.confirmed_attendance = response.confirmed_attendance
    db.commit()
    db.refresh(guest)

    return {"message": "RSVP updated", "guest": guest}
