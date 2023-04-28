from fastapi import FastAPI
from MyAviasales.views.aircraft_data import aircraft
from MyAviasales.views.flights import flights
from MyAviasales.views.bookings import bookings
from MyAviasales.views.airports import airports
from MyAviasales.views.seats import seats
from MyAviasales.views.boarding_passes import boarding_passes
from MyAviasales.views.tickets import tickets
from MyAviasales.views.ticket_flights import ticket_flights

description = """
BaluAirlines API helps you do fly to fly easily and cheaply. 🚀

Мы конечно не авиасейлс, но у нас тоже дешёвые авиабилеты

"""

app = FastAPI(
    docs_url="/",
    title="BaluAirlines",
    description=description,
    version="1.0.0",
    contact={
        "name": "Ilya Vasnev",
        "url": "https://vk.com/i.vasnev",
        "email": "ivasnev2002@gmail.com",
    }
)
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
