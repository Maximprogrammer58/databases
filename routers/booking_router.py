from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.orm_repositories import BookingRepository
from dtos.api_dtos import BookingCreate
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    return repo.get_all()

@router.get("/{booking_id}")
def get_by_id(booking_id: int, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    obj = repo.get_by_id(booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/")
def create(booking: BookingCreate, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    data = booking.dict()
    if not data.get("booking_date"):
        data["booking_date"] = datetime.now()
    obj = repo.add(repo.model(**data))
    return obj

@router.put("/{booking_id}")
def update(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    obj = repo.get_by_id(booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    obj.customer_id = booking.customer_id
    obj.flight_id = booking.flight_id
    obj.ticket_num = booking.ticket_num
    obj.booking_date = booking.booking_date or obj.booking_date
    repo.update()
    return obj

@router.delete("/{booking_id}")
def delete(booking_id: int, db: Session = Depends(get_db)):
    repo = BookingRepository(db)
    obj = repo.get_by_id(booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    repo.delete(obj)
    return {"detail": "Deleted"}
