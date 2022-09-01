import datetime
from pydantic import BaseModel, Field


# TODO: 型をもっと指定する(Optional, email, url, literalTypesなど)

# TODO: クラスは別々で指定すべきか、Optionalを使用して1つにまとめるべきか

# プランGET時
class PlanResGet(BaseModel):
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date

    class Config:
        orm_mode = True


# プラン作成
class PlanReqPost(BaseModel):
    password: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    email: str #空文字の可能性
    timestamp: datetime.date  # TODO: timestampサーバー側で管理すべきかも

class PlanResPost(BaseModel):
    plan_id: str
    timestamp: datetime.date

    class Config:
        orm_mode = True

# プラン更新
class PlanReqPut(BaseModel):
    password: str
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    timestamp: datetime.date # TODO: timestampサーバー側で管理すべきかも

class PlanResPut(BaseModel):
    timestamp: datetime.date

    class Config:
        orm_mode = True


# プラン削除
class PlanReqDelete(BaseModel):
    password: str
    plan_id: str



class SpotReq(BaseModel):
    password: str
    spot_id: int
    plan_id: str
    spot_name: str = Field(max_length=40)
    image: str
    url: str
    priority: bool
    visited: bool
    icon: int


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
    password: str
    plan_id: str
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str


class MemoRes(BaseModel):
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str

    class Config:
        orm_mode = True
