import mysql.connector
from dtos.input_dtos import AircraftModelData, FlightData
from repositories.raw_repositories import RawRepository
from services.raw_sql_service import RawSQLService
from config import MYSQL_CONFIG


conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor(dictionary=True)

aircraft_repo = RawRepository(conn, "aircraft_models", ["model_title"], "model_id")
flight_repo = RawRepository(conn, "flights", ["departure_port_id","arrival_port_id","model_id","departure_date","arrival_date"], "flight_id")

raw_service = RawSQLService(conn)

print("=== RAW SQL DEMO: Минимальный CRUD и сервисы ===")

print("\n=== Добавление модели самолета ===")
model_input = AircraftModelData(model_title=input("Название модели самолета: "))
model_id = aircraft_repo.add((model_input.model_title,))
print(f"Добавлена модель: {model_input.model_title} (ID {model_id})")

print("\n=== Добавление рейса ===")
flight_input = FlightData(
    departure_port_id=int(input("ID аэропорта вылета: ")),
    arrival_port_id=int(input("ID аэропорта прилета: ")),
    model_id=model_id,
    departure_date=input("Дата и время вылета (YYYY-MM-DD HH:MM:SS): "),
    arrival_date=input("Дата и время прибытия (YYYY-MM-DD HH:MM:SS): ")
)
flight_id = flight_repo.add((
    flight_input.departure_port_id,
    flight_input.arrival_port_id,
    flight_input.model_id,
    flight_input.departure_date,
    flight_input.arrival_date
))
print(f"Добавлен рейс ID: {flight_id}")

print("\n=== Получение всех моделей самолетов ===")
models = aircraft_repo.get_all()
for m in models:
    print(f"ID {m['model_id']}: {m['model_title']}")

model_id_to_get = int(input("\nВведите ID модели для получения: "))
model_fetched = aircraft_repo.get_by_id(model_id_to_get)
if model_fetched:
    print(f"Найдена модель: {model_fetched['model_title']} (ID {model_fetched['model_id']})")
else:
    print("Модель не найдена")

print("\n=== Обновление модели ===")
new_title = input(f"Новое название для модели (ID {model_id}): ")
aircraft_repo.update(model_id, {"model_title": new_title})
print("Модель обновлена.")

print("\n=== Удаление рейса ===")
flight_repo.delete(flight_id)
print(f"Рейс ID {flight_id} удален")

print("\n=== Демонстрация сервисов RawSQL ===")

# Query 1
airport_name = input("Введите название аэропорта для запроса 1: ")
res1 = raw_service.query1_flights_from_airport(airport_name)
print("\nQuery 1: Рейсы из аэропорта", airport_name)
for r in res1:
    print(r)

# Query 2
year = int(input("Введите год для запроса 2: "))
res2 = raw_service.query2_flight_counts(year)
print("\nQuery 2: Количество рейсов по аэропортам в", year)
for r in res2:
    print(r)

# Query 3
res3 = raw_service.query3_top_booked_flights()
print("\nQuery 3: Топ 5 рейсов по количеству бронирований")
for r in res3:
    print(r)

# Query 4
min_bookings = int(input("Введите минимальное количество бронирований для запроса 4: "))
res4 = raw_service.query4_customers_with_many_bookings(min_bookings)
print("\nQuery 4: Клиенты с бронированиями больше", min_bookings)
for r in res4:
    print(r)

# Query 5
res5 = raw_service.query5_flights_with_max_bookings()
print("\nQuery 5: Рейсы с максимальным количеством бронирований")
for r in res5:
    print(r)

# Query 6
res6 = raw_service.query6_booking_statistics()
print("\nQuery 6: Статистика бронирований по аэропортам")
for r in res6:
    print(r)

cursor.close()
conn.close()
print("\n=== DEMO завершен ===")
