from typing import Optional
from pydantic import BaseModel, validator


class Name(BaseModel):
    ru: str
    en: str


class AirportBase(BaseModel):
    airport_code: str
    airport_name: Name
    city: Name
    coordinates: str
    timezone: str

    class Config:
        orm_mode = True

    @validator('coordinates')
    def coordinates_convert(cls, v: str):
        try:
            if v[0] == '(' and v[-1] == ')':
                a = list(map(float, v[1:-1].split(',')))
                if len(a) != 2:
                    raise ValueError('coordinates not valid')
            else:
                raise ValueError('coordinates not valid')
        except:
            raise ValueError('coordinates not valid')
        return v

    @validator('airport_code')
    def airport_code_must_be_3_char(cls, v):
        if len(v) != 3:
            raise ValueError('must be 3 characters')
        return v


class AirportUpdate(BaseModel):
    airport_name: Optional[Name]
    city: Optional[Name]
    coordinates: Optional[str]
    timezone: Optional[str]
