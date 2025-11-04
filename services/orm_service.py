from sqlalchemy.orm import aliased
from sqlalchemy import func
from models.models import Flight, Airport, Booking, Customer, AircraftModel
from typing import List


class ORMService:
    def __init__(self, session):
        self.session = session

    def query1_flights_from_airport(self, airport_name: str) -> List[dict]:
        dep = aliased(Airport)
        arr = aliased(Airport)

        query = self.session.query(
            dep.title.label("departure_airport"),
            arr.title.label("arrival_airport"),
            AircraftModel.model_title,
            Flight.departure_date,
            Flight.arrival_date
        ).join(dep, Flight.departure_airport) \
            .join(arr, Flight.arrival_airport) \
            .join(AircraftModel, Flight.model) \
            .filter(dep.title == airport_name)

        result = query.all()
        return [
            {
                "departure_airport": row.departure_airport,
                "arrival_airport": row.arrival_airport,
                "model_title": row.model_title,
                "departure_date": row.departure_date,
                "arrival_date": row.arrival_date
            }
            for row in result
        ]

    def query2_flight_counts(self, year: int) -> List[dict]:
        query = self.session.query(
            Airport.title.label("airport_name"),
            func.count(Flight.flight_id).label("count")
        ).outerjoin(
            Flight, (Flight.departure_port_id == Airport.port_id) & (func.year(Flight.departure_date) == year)
        ).group_by(Airport.port_id, Airport.title) \
            .order_by(func.count(Flight.flight_id).desc())

        result = query.all()
        return [{"airport_name": row.airport_name, "count": row.count} for row in result]

    def query3_top_booked_flights(self) -> List[dict]:
        dep = aliased(Airport)
        arr = aliased(Airport)

        query = self.session.query(
            dep.title.label("departure_airport"),
            arr.title.label("arrival_airport"),
            Flight.departure_date,
            func.count(Booking.booking_id).label("count")
        ).join(dep, Flight.departure_airport) \
            .join(arr, Flight.arrival_airport) \
            .join(Booking) \
            .group_by(Flight.flight_id) \
            .order_by(func.count(Booking.booking_id).desc()) \
            .limit(5)

        result = query.all()
        return [
            {
                "departure_airport": row.departure_airport,
                "arrival_airport": row.arrival_airport,
                "departure_date": row.departure_date,
                "count": row.count
            }
            for row in result
        ]

    def query4_customers_with_many_bookings(self, min_bookings: int) -> List[dict]:
        query = self.session.query(
            Customer.first_name,
            Customer.last_name,
            func.count(Booking.booking_id).label("count")
        ).join(Booking) \
            .group_by(Customer.customer_id) \
            .having(func.count(Booking.booking_id) > min_bookings) \
            .order_by(Customer.last_name, Customer.first_name)

        result = query.all()
        return [
            {
                "first_name": row.first_name,
                "last_name": row.last_name,
                "count": row.count
            }
            for row in result
        ]

    def query5_flights_with_max_bookings(self) -> List[dict]:
        subq = self.session.query(
            Booking.flight_id,
            func.count(Booking.booking_id).label("cnt")
        ).group_by(Booking.flight_id).subquery()

        max_cnt = self.session.query(func.max(subq.c.cnt)).scalar()

        query = self.session.query(Flight.flight_id) \
            .join(Booking) \
            .group_by(Flight.flight_id) \
            .having(func.count(Booking.booking_id) == max_cnt)

        result = query.all()
        return [{"flight_id": row.flight_id} for row in result]

    def query6_booking_statistics(self) -> List[dict]:
        subq = self.session.query(
            Flight.departure_port_id,
            func.count(Booking.booking_id).label("cnt")
        ).outerjoin(Booking).group_by(Flight.flight_id, Flight.departure_port_id).subquery()

        query = self.session.query(
            Airport.title.label("departure_airport"),
            func.coalesce(func.min(subq.c.cnt), 0).label("min"),
            func.coalesce(func.avg(subq.c.cnt), 0).label("avg"),
            func.coalesce(func.max(subq.c.cnt), 0).label("max")
        ).outerjoin(subq, Airport.port_id == subq.c.departure_port_id) \
            .group_by(Airport.port_id, Airport.title)

        result = query.all()
        return [
            {
                "departure_airport": row.departure_airport,
                "min": row.min,
                "avg": row.avg,
                "max": row.max
            }
            for row in result
        ]
