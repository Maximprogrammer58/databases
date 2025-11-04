from sqlalchemy.orm import aliased
from sqlalchemy import func
from models.models import Flight, Airport, Booking, Customer, AircraftModel

class ORMService:
    def __init__(self, session):
        self.session = session

    def query1_flights_from_airport(self, airport_name):
        dep = aliased(Airport)
        arr = aliased(Airport)
        return self.session.query(
            dep.title.label("departure_airport"),
            arr.title.label("arrival_airport"),
            AircraftModel.model_title,
            Flight.departure_date,
            Flight.arrival_date
        ).join(dep, Flight.departure_airport)\
         .join(arr, Flight.arrival_airport)\
         .join(AircraftModel, Flight.model)\
         .filter(dep.title == airport_name)\
         .all()

    def query2_flight_counts(self, year):
        return self.session.query(
            Airport.title.label("airport_name"),
            func.count(Flight.flight_id).label("count")
        ).outerjoin(
            Flight, (Flight.departure_port_id == Airport.port_id) & (func.year(Flight.departure_date) == year)
        ).group_by(Airport.port_id, Airport.title)\
         .order_by(func.count(Flight.flight_id).desc())\
         .all()

    def query3_top_booked_flights(self):
        dep = aliased(Airport)
        arr = aliased(Airport)
        return self.session.query(
            dep.title.label("departure_airport"),
            arr.title.label("arrival_airport"),
            Flight.departure_date,
            func.count(Booking.booking_id).label("count")
        ).join(dep, Flight.departure_airport)\
         .join(arr, Flight.arrival_airport)\
         .join(Booking)\
         .group_by(Flight.flight_id)\
         .order_by(func.count(Booking.booking_id).desc())\
         .limit(5)\
         .all()

    def query4_customers_with_many_bookings(self, min_bookings):
        return self.session.query(
            Customer.first_name,
            Customer.last_name,
            func.count(Booking.booking_id).label("count")
        ).join(Booking)\
         .group_by(Customer.customer_id)\
         .having(func.count(Booking.booking_id) > min_bookings)\
         .order_by(Customer.last_name, Customer.first_name)\
         .all()

    def query5_flights_with_max_bookings(self):
        subq = self.session.query(
            Booking.flight_id,
            func.count(Booking.booking_id).label("cnt")
        ).group_by(Booking.flight_id).subquery()
        max_cnt = self.session.query(func.max(subq.c.cnt)).scalar()

        return self.session.query(Flight.flight_id)\
            .join(Booking)\
            .group_by(Flight.flight_id)\
            .having(func.count(Booking.booking_id) == max_cnt)\
            .all()

    def query6_booking_statistics(self):
        subq = self.session.query(
            Flight.departure_port_id,
            func.count(Booking.booking_id).label("cnt")
        ).outerjoin(Booking).group_by(Flight.flight_id, Flight.departure_port_id).subquery()

        return self.session.query(
            Airport.title.label("departure_airport"),
            func.coalesce(func.min(subq.c.cnt), 0).label("min"),
            func.coalesce(func.avg(subq.c.cnt), 0).label("avg"),
            func.coalesce(func.max(subq.c.cnt), 0).label("max")
        ).outerjoin(subq, Airport.port_id == subq.c.departure_port_id)\
         .group_by(Airport.port_id, Airport.title)\
         .all()
