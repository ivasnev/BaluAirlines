from fastapi import Depends, FastAPI
from MyAviasales.views.aircraft_data import aircraft
from MyAviasales.views.flights import flights
from MyAviasales.views.bookings import bookings
from MyAviasales.views.airports import airports
app = FastAPI()
app.include_router(aircraft.router)
app.include_router(flights.router)
app.include_router(airports.router)
# app.include_router(boarding_passes.router)
app.include_router(bookings.router)
# app.include_router(seats.router)
# app.include_router(tickets.router)
# app.include_router(ticket_flights.router)


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
