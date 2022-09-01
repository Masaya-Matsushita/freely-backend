import datetime
from pydantic import BaseModel, Field


# TODO: 型をもっと指定する(Optional, email, url, literalTypesなど)

class PlanReq(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    verify_key: str
    email: str
    timestamp: datetime.date
    password: str

class PlanRes(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    verify_key: str
    email: str
    timestamp: datetime.date

    class Config:
        orm_mode = True


class SpotReq(BaseModel):
    spot_id: int
    plan_id: str
    spot_name: str = Field(max_length=40)
    image: str
    url: str
    priority: bool
    visited: bool
    icon: int
    password: str


class SpotRes(BaseModel):
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


class MemoReq(BaseModel):
    plan_id: str
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str
    password: str


class MemoRes(BaseModel):
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str

    class Config:
        orm_mode = True
