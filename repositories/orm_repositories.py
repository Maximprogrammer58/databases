from models.models import AircraftModel, Airport, Flight, Customer, Booking


class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_all(self):
        return self.session.query(self.model).all()

    def get_by_id(self, _id):
        return self.session.query(self.model).get(_id)

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self):
        self.session.commit()

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()


class AircraftModelRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, AircraftModel)


class AirportRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Airport)


class FlightRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Flight)


class CustomerRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Customer)


class BookingRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Booking)
