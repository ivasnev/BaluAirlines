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
from datetime import datetime


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

    @validator('departure_airport', 'arrival_airport')
    def airport_code_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('airport code must be 3 characters')
        return v

    @validator('flight_no')
    def flight_no_must_be_6_char(cls, v):
        if len(v) != 6:
            raise ValueError('must be 6 characters')
        return v


class FlightPostResponse(FlightBase):
    flight_id: int


class FlightUpdate(BaseModel):
    scheduled_departure: Optional[datetime]
    scheduled_arrival: Optional[datetime]
    departure_airport: Optional[str]
    arrival_airport: Optional[str]
    status: Optional[str]
    aircraft_code: Optional[str]
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]


class FlightPathBase(BaseModel):
    flight_id: int
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


class FlightPath(BaseModel):
    fare_condition: str
    num_of_passengers: int
    cost: float
    time: str
    flights: List[FlightPathBase]

    @validator('fare_condition')
    def fare_conditions_one_of(cls, v):
        enum = ['Economy', 'Comfort', 'Business']
        if v in enum:
            return v
        raise ValueError('must be Economy, Comfort or Business')
