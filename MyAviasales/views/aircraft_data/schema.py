from typing import Optional
from pydantic import BaseModel, validator


class Model(BaseModel):
    ru: str
    en: str


class AircraftBase(BaseModel):
    aircraft_code: str
    model: Model
    range: int

    class Config:
        orm_mode = True

    @validator('aircraft_code')
    def aircraft_code_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('must be 3 characters')
        return v

    @validator('range')
    def range_must_be_more_0(cls, v):
        if v <= 0:
            raise ValueError('must be more than 0')
        return v


class AircraftUpdate(BaseModel):
    model: Optional[Model]
    range: Optional[int]

    @validator('range')
    def range_must_be_more_0(cls, v):
        if v <= 0:
            raise ValueError('must be more than 0')
        return v
