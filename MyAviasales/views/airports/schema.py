from typing import Optional
from pydantic import BaseModel, validator


class Name(BaseModel):
    ru: str
    en: str


class AirportBase(BaseModel):
    airport_code: str
    airport_name: Name
    city: Name
    coordinates: tuple
    timezone: str

    class Config:
        orm_mode = True

    @validator('airport_code')
    def airport_code_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('must be 3 characters')
        return v


class AirportUpdate(BaseModel):
    airport_name: Optional[Name]
    city: Optional[Name]
    coordinates: Optional[tuple]
    timezone: Optional[str]
