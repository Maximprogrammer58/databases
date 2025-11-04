from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.orm_service import ORMService

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/flights_from_airport")
def flights_from_airport(airport_name: str = Query(..., description="Название аэропорта"),
                         db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query1_flights_from_airport(airport_name)

@router.get("/flight_counts")
def flight_counts(year: int = Query(..., description="Год для подсчета рейсов"),
                  db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query2_flight_counts(year)

@router.get("/top_booked_flights")
def top_booked_flights(db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query3_top_booked_flights()

@router.get("/customers_with_many_bookings")
def customers_with_many_bookings(min_bookings: int = Query(..., description="Минимальное количество бронирований"),
                                 db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query4_customers_with_many_bookings(min_bookings)

@router.get("/flights_with_max_bookings")
def flights_with_max_bookings(db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query5_flights_with_max_bookings()

@router.get("/booking_statistics")
def booking_statistics(db: Session = Depends(get_db)):
    service = ORMService(db)
    return service.query6_booking_statistics()
