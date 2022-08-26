import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

class Plan(BaseModel):
    plan_id: str
    plan_name: str = Field(max_length=40)
    start_date: datetime.date
    end_date: datetime.date
    verify_key: str
    email: str
    timestamp: datetime.date

class Spot(BaseModel):
    spot_id: int
    plan_id: str
    spot_name: str = Field(max_length=40)
    image: str
    url: str
    priority: bool
    visited: bool
    icon: str

class Memo(BaseModel):
    memo_id: int
    spot_id: int
    text: str = Field(max_length=150)
    marked: str


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HelloWorld"}

@app.post("/plans")
async def plans(plans: Plan):
    return {"plans": plans}

@app.post("/spots")
async def spots(spots: Spot):
    return {"spots": spots}

@app.post("/memos")
async def memos(memos: Memo):
    return {"memos": memos}
