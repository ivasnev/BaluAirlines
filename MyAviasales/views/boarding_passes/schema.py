from typing import Optional
from pydantic import BaseModel, validator


class BoardingPassBase(BaseModel):
    ticket_no: str
    flight_id: int
    boarding_no: int
    seat_no: str

    class Config:
        orm_mode = True

    @validator('seat_no')
    def seat_no_must_be_2or3_char(cls, v):
        if 2 <= len(v) <= 3:
            return v
        raise ValueError('must be 3 characters')

    @validator('ticket_no')
    def ticket_no_must_be_less_5_char(cls, v):
        if len(v) >= 14:
            raise ValueError('must be less 14 characters')
        return v


class BoardingPassPost(BaseModel):
    ticket_no: str
    flight_id: int
    seat_no: str

    @validator('seat_no')
    def seat_no_must_be_2or3_char(cls, v):
        if 2 <= len(v) <= 3:
            return v
        raise ValueError('must be 3 characters')

    @validator('ticket_no')
    def ticket_no_must_be_less_5_char(cls, v):
        if len(v) >= 14:
            raise ValueError('must be less 14 characters')
        return v


class BoardingPassUpdate(BaseModel):
    seat_no: Optional[str]

    @validator('seat_no')
    def seat_no_must_be_2or3_char(cls, v):
        if 2 <= len(v) <= 3:
            return v
        raise ValueError('must be 3 characters')
