from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime
from MyAviasales.views.tickets.schema import TicketBase


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


class BookingResponse(BookingBase):
    tickets: Optional[List[TicketBase]]


class BookingUpdate(BaseModel):
    book_date: Optional[datetime]
    total_amount: Optional[float]
