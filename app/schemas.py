import datetime
from pydantic import BaseModel, Field


class Plan(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    verify_key: str
    email: str
    timestamp: datetime.date

    class Config:
        orm_mode = True


class Spot(BaseModel):
    spot_id: int
    plan_id: str
    spot_name: str = Field(max_length=40)
    image: str
    url: str
    priority: bool
    visited: bool
    icon: int

    class Config:
        orm_mode = True


class Memo(BaseModel):
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str

    class Config:
        orm_mode = True
