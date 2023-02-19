# class WithCustomEncoders(BaseModel):
#     dt: datetime
#     diff: timedelta
#
#     class Config:
#         json_encoders = {
#             datetime: lambda v: v.timestamp(),
#             timedelta: timedelta_isoformat,
#         }

from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime, timedelta


class FlightBase(BaseModel):
    flight_no: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    departure_airport: str
    arrival_airport: str
    status: str
    aircraft_code: str
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]

    class Config:
        orm_mode = True

    @validator('flight_no')
    def flight_no_must_be_6_char(cls, v):
        if len(v) != 6:
            raise ValueError('must be 6 characters')
        return v


class FlightUpdate(BaseModel):
    scheduled_departure: Optional[datetime]
    scheduled_arrival: Optional[datetime]
    departure_airport: Optional[str]
    arrival_airport: Optional[str]
    status: Optional[str]
    aircraft_code: Optional[str]
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]


class FlightPath(BaseModel):
    cost: float
    time: str
    flights: List[FlightBase]
