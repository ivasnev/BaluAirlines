from typing import Optional
from pydantic import BaseModel, validator


class SeatBase(BaseModel):
    aircraft_code: str
    seat_no: str
    fare_conditions: str

    class Config:
        orm_mode = True

    @validator('aircraft_code')
    def aircraft_code_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('must be 3 characters')
        return v

    @validator('seat_no')
    def seat_no_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('must be 3 characters')
        return v

    @validator('fare_conditions')
    def fare_conditions_one_of(cls, v):
        enum = ['Economy', 'Comfort', 'Business']
        if v in enum:
            return v
        raise ValueError('must be 3 characters')


class SeatUpdate(BaseModel):
    fare_conditions: Optional[str]

    @validator('fare_conditions')
    def fare_conditions_one_of(cls, v):
        enum = ['Economy', 'Comfort', 'Business']
        if v in enum:
            return v
        raise ValueError('must be Economy, Comfort or Business')
