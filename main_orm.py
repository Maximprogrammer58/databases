from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dtos.input_dtos import AircraftModelData, FlightData
from models.models import Base, AircraftModel, Flight, Airport, Customer, Booking
from repositories.orm_repositories import AircraftModelRepository, FlightRepository
from services.orm_service import ORMService
from config import DB_URL


engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

aircraft_repo = AircraftModelRepository(session)
flight_repo = FlightRepository(session)

orm_service = ORMService(session)

print("=== ORM DEMO: CRUD и сервисы ===")

print("\n=== Добавление модели самолета ===")
model_input = AircraftModelData(model_title=input("Название модели самолета: "))
model = aircraft_repo.add(AircraftModel(**model_input.__dict__))
print(f"Добавлена модель: {model.model_title} (ID {model.model_id})")

print("\n=== Добавление рейса ===")
flight_input = FlightData(
    departure_port_id=int(input("ID аэропорта вылета: ")),
    arrival_port_id=int(input("ID аэропорта прилета: ")),
    model_id=model.model_id,
    departure_date=input("Дата и время вылета (YYYY-MM-DD HH:MM:SS): "),
    arrival_date=input("Дата и время прибытия (YYYY-MM-DD HH:MM:SS): ")
)
flight = flight_repo.add(Flight(
    departure_port_id=flight_input.departure_port_id,
    arrival_port_id=flight_input.arrival_port_id,
    model_id=flight_input.model_id,
    departure_date=datetime.strptime(flight_input.departure_date, "%Y-%m-%d %H:%M:%S"),
    arrival_date=datetime.strptime(flight_input.arrival_date, "%Y-%m-%d %H:%M:%S")
))
print(f"Добавлен рейс ID: {flight.flight_id}")

print("\n=== Получение всех моделей самолетов ===")
models = aircraft_repo.get_all()
for m in models:
    print(f"ID {m.model_id}: {m.model_title}")

model_id_to_get = int(input("\nВведите ID модели для получения: "))
model_fetched = aircraft_repo.get_by_id(model_id_to_get)
if model_fetched:
    print(f"Найдена модель: {model_fetched.model_title} (ID {model_fetched.model_id})")
else:
    print("Модель не найдена")

print("\n=== Обновление модели ===")
model_to_update = aircraft_repo.get_by_id(model.model_id)
new_title = input(f"Новое название для модели '{model_to_update.model_title}': ")
model_to_update.model_title = new_title
aircraft_repo.update()
print(f"Модель обновлена: {model_to_update.model_title}")

print("\n=== Удаление рейса ===")
flight_repo.delete(flight)
print(f"Рейс ID {flight.flight_id} удален")

print("\n=== Демонстрация сервисов ORM ===")

# Query 1
airport_name = input("Введите название аэропорта для запроса 1: ")
res1 = orm_service.query1_flights_from_airport(airport_name)
print("\nQuery 1: Рейсы из аэропорта", airport_name)
for r in res1:
    print(r)

# Query 2
year = int(input("Введите год для запроса 2: "))
res2 = orm_service.query2_flight_counts(year)
print("\nQuery 2: Количество рейсов по аэропортам в", year)
for r in res2:
    print(r)

# Query 3
res3 = orm_service.query3_top_booked_flights()
print("\nQuery 3: Топ 5 рейсов по количеству бронирований")
for r in res3:
    print(r)

# Query 4
min_bookings = int(input("Введите минимальное количество бронирований для запроса 4: "))
res4 = orm_service.query4_customers_with_many_bookings(min_bookings)
print("\nQuery 4: Клиенты с бронированиями больше", min_bookings)
for r in res4:
    print(r)

# Query 5
res5 = orm_service.query5_flights_with_max_bookings()
print("\nQuery 5: Рейсы с максимальным количеством бронирований")
for r in res5:
    print(r)

# Query 6
res6 = orm_service.query6_booking_statistics()
print("\nQuery 6: Статистика бронирований по аэропортам")
for r in res6:
    print(r)

session.close()
print("\n=== DEMO завершен ===")
