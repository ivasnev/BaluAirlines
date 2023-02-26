from typing import Optional
from pydantic import BaseModel, validator


class TicketFlightBase(BaseModel):
    flight_id: int
    ticket_no: str
    fare_conditions: str
    amount: float

    class Config:
        orm_mode = True

    @validator('ticket_no')
    def ticket_no_must_less_14_char(cls, v):
        if len(v) > 13:
            raise ValueError('must be less 14 characters')
        return v

    @validator('fare_conditions')
    def fare_conditions_one_of(cls, v):
        enum = ['Economy', 'Comfort', 'Business']
        if v in enum:
            return v
        raise ValueError('must be 3 characters')


class TicketFlightUpdate(BaseModel):
    amount: Optional[float]
