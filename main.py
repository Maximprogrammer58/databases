from fastapi import FastAPI
from routers import (
    aircraft_model_router,
    airport_router,
    customer_router,
    flight_router,
    booking_router,
    service_router,
)

app = FastAPI(title="Airline Booking API")

app.include_router(aircraft_model_router.router, prefix="/aircraft-models", tags=["Aircraft Models"])
app.include_router(airport_router.router, prefix="/airports", tags=["Airports"])
app.include_router(customer_router.router, prefix="/customers", tags=["Customers"])
app.include_router(flight_router.router, prefix="/flights", tags=["Flights"])
app.include_router(booking_router.router, prefix="/bookings", tags=["Bookings"])
app.include_router(service_router.router, prefix="/services", tags=["Services"])

@app.get("/")
def root():
    return {"message": "Airline Booking API работает!"}
