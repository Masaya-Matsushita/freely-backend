import datetime
from typing import Literal
from pydantic import BaseModel, Field


# TODO: 型をもっと指定する(Optional, email, url, literalTypesなど)

# TODO: クラスは別々で指定すべきか、Optionalを使用して1つにまとめるべきか


# テスト用
class PlanTest(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    verify_key: str
    email: str
    timestamp: datetime.date

    class Config:
        orm_mode = True


class SpotTest(BaseModel):
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str
    icon: int
    url: str
    priority: bool
    visited: bool

    class Config:
        orm_mode = True


class MemoTest(BaseModel):
    spot_id: int
    memo_id: int
    text: str = Field(max_length=150)
    marked: str

    class Config:
        orm_mode = True


# 履歴GET時(≠プラン)
class PlanResHistory(BaseModel):
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    timestamp: datetime.date

    class Config:
        orm_mode = True

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
    email: str #空文字の可能性あり
    timestamp: datetime.date  # TODO: timestampサーバー側で管理すべきかも

class PlanResPost(BaseModel):
    plan_id: str

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


# プラン削除
class PlanReqDelete(BaseModel):
    password: str
    plan_id: str



# スポットGET時
class SpotResGet(BaseModel):
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str #空文字の可能性あり
    icon: int #0の可能性あり
    url: str #空文字の可能性あり
    priority: bool
    visited: bool

    class Config:
        orm_mode = True


# スポット作成
class SpotReqPost(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str #空文字の可能性あり
    icon: int #0の可能性あり
    url: str #空文字の可能性あり


# スポット更新
class SpotReqPutBody(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str #空文字の可能性あり
    icon: int #0の可能性あり
    url: str #空文字の可能性あり

# Priority更新
# TODO: swrの挙動次第ではresponseすべきかも
class SpotReqPutPriority(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    priority: bool

# visited更新
# TODO: swrの挙動次第ではresponseすべきかも
class SpotReqPutVisited(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    visited: bool


# スポット削除
class SpotReqDelete(BaseModel):
    password: str
    plan_id: str
    spot_id: int



# メモGET時
class MemoResGet(BaseModel):
    spot_id: int
    memo_id: int
    text: str = Field(max_length=150)
    marked: Literal['red', 'green', 'none']

    class Config:
        orm_mode = True


# メモ作成
class MemoReqPost(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    text: str = Field(max_length=150)
    marked: Literal['red', 'green', 'none']


# メモ削除
class MemoReqDelete(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    memo_id: int
