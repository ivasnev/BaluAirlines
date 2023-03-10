from fastapi import FastAPI
from MyAviasales.views.aircraft_data import aircraft
from MyAviasales.views.flights import flights
from MyAviasales.views.bookings import bookings
from MyAviasales.views.airports import airports
from MyAviasales.views.seats import seats
from MyAviasales.views.boarding_passes import boarding_passes
from MyAviasales.views.tickets import tickets
from MyAviasales.views.ticket_flights import ticket_flights
app = FastAPI()
app.include_router(aircraft.router)
app.include_router(flights.router)
app.include_router(airports.router)
app.include_router(boarding_passes.router)
app.include_router(bookings.router)
app.include_router(seats.router)
app.include_router(tickets.router)
app.include_router(ticket_flights.router)


# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
