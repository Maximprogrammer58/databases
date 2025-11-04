from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.orm_repositories import AirportRepository
from dtos.api_dtos import AirportCreate

router = APIRouter(prefix="/airports", tags=["Airports"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    repo = AirportRepository(db)
    return repo.get_all()

@router.get("/{airport_id}")
def get_by_id(airport_id: int, db: Session = Depends(get_db)):
    repo = AirportRepository(db)
    obj = repo.get_by_id(airport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/")
def create(airport: AirportCreate, db: Session = Depends(get_db)):
    repo = AirportRepository(db)
    obj = repo.add(repo.model(**airport.dict()))
    return obj

@router.put("/{airport_id}")
def update(airport_id: int, airport: AirportCreate, db: Session = Depends(get_db)):
    repo = AirportRepository(db)
    obj = repo.get_by_id(airport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.title = airport.title
    obj.lat = airport.lat
    obj.lon = airport.lon
    obj.notes = airport.notes
    repo.update()
    return obj

@router.delete("/{airport_id}")
def delete(airport_id: int, db: Session = Depends(get_db)):
    repo = AirportRepository(db)
    obj = repo.get_by_id(airport_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    repo.delete(obj)
    return {"detail": "Deleted"}
