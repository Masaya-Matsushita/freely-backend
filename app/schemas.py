from typing import Literal, Optional
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
    icon: Optional[Literal['Spot', 'Restaurant', 'Souvenir', 'Hotel']]
    image: str
    priority: bool
    visited: bool

    class Config:
        orm_mode = True


class MemoTest(BaseModel):
    plan_id: str
    spot_id: int
    memo_id: int
    text: str = Field(max_length=100)
    marked: Literal['White', 'Red', 'Green']

    class Config:
        orm_mode = True


# パスワード認証
class AuthUser(BaseModel):
    password: str
    plan_id: str


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
    password: Optional[str]
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: str
    end_date: str


# プラン削除
class PlanReqDelete(BaseModel):
    password: Optional[str]
    plan_id: str



# スポットGET時
class SpotResGet(BaseModel):
    spot_name: str = Field(max_length=40)
    icon: Optional[Literal['Spot', 'Restaurant', 'Souvenir', 'Hotel']]
    image: str

    class Config:
        orm_mode = True


# スポットリストGET時
class SpotListResGet(BaseModel):
    plan_id: str # 必要ない？
    spot_id: int
    spot_name: str = Field(max_length=40)
    icon: Optional[Literal['Spot', 'Restaurant', 'Souvenir', 'Hotel']]
    image: str
    priority: bool
    visited: bool

    class Config:
        orm_mode = True


# スポット作成
class SpotReqPost(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_name: str = Field(max_length=40)
    icon: Optional[Literal['Spot', 'Restaurant', 'Souvenir', 'Hotel']]
    image: str


# スポット更新
class SpotReqPutBody(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int
    spot_name: str = Field(max_length=40)
    icon: Optional[Literal['Spot', 'Restaurant', 'Souvenir', 'Hotel']]
    image: str


# Priority更新
# TODO: swrの挙動次第ではresponseすべきかも
class SpotReqPutPriority(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int
    priority: bool

# visited更新
# TODO: swrの挙動次第ではresponseすべきかも
class SpotReqPutVisited(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int
    visited: bool


# スポット削除
class SpotReqDelete(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int



# メモリストGET時
class MemoListResGet(BaseModel):
    plan_id: str
    spot_id: int
    memo_id: int
    text: str = Field(max_length=100)
    marked: Literal['White', 'Red', 'Green']

    class Config:
        orm_mode = True


# メモ作成
class MemoReqPost(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int
    text: str = Field(max_length=100)
    marked: Literal['White', 'Red', 'Green']


# メモ削除
class MemoReqDelete(BaseModel):
    password: Optional[str]
    plan_id: str
    spot_id: int
    memo_id: int
