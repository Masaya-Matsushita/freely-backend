from typing import Literal
from pydantic import BaseModel, Field

# テスト用
class PlanTest(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: str
    end_date: str
    verify_key: str

    class Config:
        orm_mode = True


class SpotTest(BaseModel):
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str
    icon: Literal['', 'Spot', 'Restaurant', 'Souvenir', 'Hotel']
    priority: bool
    visited: bool

    class Config:
        orm_mode = True


class MemoTest(BaseModel):
    spot_id: int
    memo_id: int
    text: str = Field(max_length=150)
    marked: Literal['White', 'Red', 'Green']

    class Config:
        orm_mode = True


# パスワード認証
class AuthUser(BaseModel):
    plan_id: str
    password: str


# プランGET時
class PlanResGet(BaseModel):
    plan_name: str = Field(max_length=40)
    start_date: str
    end_date: str

    class Config:
        orm_mode = True


# プラン作成
class PlanReqPost(BaseModel):
    password: str
    plan_name: str = Field(max_length=40)
    start_date: str
    end_date: str

class PlanResPost(BaseModel):
    plan_id: str

    class Config:
        orm_mode = True

# プラン更新
class PlanReqPut(BaseModel):
    password: str
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: str
    end_date: str


# プラン削除
class PlanReqDelete(BaseModel):
    password: str
    plan_id: str



# スポットGET時
class SpotResGet(BaseModel):
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str #空文字の可能性あり
    icon: Literal['', 'Spot', 'Restaurant', 'Souvenir', 'Hotel']
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
    icon: Literal['', 'Spot', 'Restaurant', 'Souvenir', 'Hotel']


# スポット更新
class SpotReqPutBody(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    image: str #空文字の可能性あり
    icon: Literal['', 'Spot', 'Restaurant', 'Souvenir', 'Hotel']


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
    marked: Literal['White', 'Red', 'Green']

    class Config:
        orm_mode = True


# メモ作成
class MemoReqPost(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    text: str = Field(max_length=150)
    marked: Literal['White', 'Red', 'Green']


# メモ削除
class MemoReqDelete(BaseModel):
    password: str
    plan_id: str
    spot_id: int
    memo_id: int
