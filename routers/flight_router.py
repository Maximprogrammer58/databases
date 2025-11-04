from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.orm_repositories import FlightRepository
from dtos.api_dtos import FlightCreate
from datetime import datetime

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    repo = FlightRepository(db)
    return repo.get_all()

@router.get("/{flight_id}")
def get_by_id(flight_id: int, db: Session = Depends(get_db)):
    repo = FlightRepository(db)
    obj = repo.get_by_id(flight_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/")
def create(flight: FlightCreate, db: Session = Depends(get_db)):
    repo = FlightRepository(db)
    obj = repo.add(repo.model(**flight.dict()))
    return obj

@router.put("/{flight_id}")
def update(flight_id: int, flight: FlightCreate, db: Session = Depends(get_db)):
    repo = FlightRepository(db)
    obj = repo.get_by_id(flight_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.departure_port_id = flight.departure_port_id
    obj.arrival_port_id = flight.arrival_port_id
    obj.model_id = flight.model_id
    obj.departure_date = flight.departure_date
    obj.arrival_date = flight.arrival_date
    repo.update()
    return obj

@router.delete("/{flight_id}")
def delete(flight_id: int, db: Session = Depends(get_db)):
    repo = FlightRepository(db)
    obj = repo.get_by_id(flight_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    repo.delete(obj)
    return {"detail": "Deleted"}
