from typing import Optional, List
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from MyAviasales.views.tickets.schema import TicketBase


class ContactData(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]


class BookingBase(BaseModel):
    book_ref: str
    book_date: datetime
    total_amount: float

    class Config:
        orm_mode = True

    @validator('book_ref')
    def book_ref_must_be_less_7_char(cls, v):
        if len(v) >= 7:
            raise ValueError('must be less 7 characters')
        return v


class Passenger(BaseModel):
    passenger_id: str
    passenger_name: str
    contact_data: Optional[ContactData]

    @validator('passenger_id')
    def passenger_id_must_less_20_char(cls, v):
        if len(v) > 20:
            raise ValueError('must be less 20 characters')
        return v


class BookingPostRequest(BaseModel):
    fare_condition: str
    flights: List[int]
    passengers: List[Passenger]

    @validator('fare_condition')
    def fare_conditions_one_of(cls, v):
        enum = ['Economy', 'Comfort', 'Business']
        if v in enum:
            return v
        raise ValueError('must be Economy, Comfort or Business')


class BookingResponse(BookingBase):
    tickets: Optional[List[TicketBase]]


class BookingUpdate(BaseModel):
    book_date: Optional[datetime]
    total_amount: Optional[float]
