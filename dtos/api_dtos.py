from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AircraftModelCreate(BaseModel):
    model_title: str


class AirportCreate(BaseModel):
    title: str
    lat: float
    lon: float
    notes: Optional[str] = None


class CustomerCreate(BaseModel):
    passport: str
    first_name: str
    last_name: str
    phone: Optional[str] = None


class FlightCreate(BaseModel):
    departure_port_id: int
    arrival_port_id: int
    model_id: int
    departure_date: datetime
    arrival_date: datetime


class BookingCreate(BaseModel):
    customer_id: int
    flight_id: int
    ticket_num: str
    booking_date: Optional[datetime] = None
