from typing import Optional
from pydantic import BaseModel, validator, EmailStr


class ContactData(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]


class TicketBase(BaseModel):
    ticket_no: str
    book_ref: str
    passenger_id: str
    passenger_name: str
    contact_data: Optional[ContactData]

    class Config:
        orm_mode = True

    @validator('ticket_no')
    def ticket_no_must_less_14_char(cls, v):
        if len(v) > 13:
            raise ValueError('must be less 14 characters')
        return v

    @validator('book_ref')
    def book_ref_must_be_less_7_char(cls, v):
        if len(v) >= 7:
            raise ValueError('must be less 7 characters')
        return v

    @validator('passenger_id')
    def passenger_id_must_less_20_char(cls, v):
        if len(v) > 20:
            raise ValueError('must be less 20 characters')
        return v


class TicketUpdate(BaseModel):
    passenger_id: Optional[str]
    passenger_name: Optional[str]
    contact_data: Optional[ContactData]
    amount: Optional[float]
