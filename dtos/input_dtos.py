from dataclasses import dataclass
from datetime import datetime


@dataclass
class AirportData:
    title: str
    lat: float
    lon: float
    notes: str = None


@dataclass
class AircraftModelData:
    model_title: str


@dataclass
class CustomerData:
    passport: str
    first_name: str
    last_name: str
    phone: str


@dataclass
class FlightData:
    departure_port_id: int
    arrival_port_id: int
    model_id: int
    departure_date: str  # "YYYY-MM-DD HH:MM:SS"
    arrival_date: str    # "YYYY-MM-DD HH:MM:SS"


@dataclass
class BookingData:
    customer_id: int
    flight_id: int
    ticket_num: str
    booking_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
