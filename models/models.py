from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class AircraftModel(Base):
    __tablename__ = 'aircraft_models'
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_title = Column(String(100), nullable=False)
    flights = relationship("Flight", back_populates="model")


class Airport(Base):
    __tablename__ = 'airports'
    port_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    lat = Column(DECIMAL(9,6), nullable=False)
    lon = Column(DECIMAL(9,6), nullable=False)
    notes = Column(JSON)
    departures = relationship("Flight", foreign_keys="Flight.departure_port_id", back_populates="departure_airport")
    arrivals = relationship("Flight", foreign_keys="Flight.arrival_port_id", back_populates="arrival_airport")


class Flight(Base):
    __tablename__ = 'flights'
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    departure_port_id = Column(Integer, ForeignKey('airports.port_id'), nullable=False)
    arrival_port_id = Column(Integer, ForeignKey('airports.port_id'), nullable=False)
    model_id = Column(Integer, ForeignKey('aircraft_models.model_id'), nullable=False)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    departure_airport = relationship("Airport", foreign_keys=[departure_port_id], back_populates="departures")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_port_id], back_populates="arrivals")
    model = relationship("AircraftModel", back_populates="flights")
    bookings = relationship("Booking", back_populates="flight")


class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    passport = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    bookings = relationship("Booking", back_populates="customer")


class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), nullable=False)
    ticket_num = Column(String(20), unique=True, nullable=False)
    booking_date = Column(DateTime, default=datetime.now)
    customer = relationship("Customer", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
