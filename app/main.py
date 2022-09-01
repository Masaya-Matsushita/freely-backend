from typing import List, Union, Literal
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# with句で書き換え？
# https://fastapi.tiangolo.com/ja/tutorial/dependencies/dependencies-with-yield/
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# test
@app.get("/")
def read_root():
    return {"message": "HelloWorld"}


# GET
@app.get("/plan", response_model=schemas.PlanRes)
async def get_plan(plan_id: str = 'default', db: Session = Depends(get_db)):
    plan = crud.get_plan(db=db, plan_id=plan_id)
    return plan

@app.get("/spot", response_model=List[schemas.SpotRes])
async def get_spots(plan_id: str = 'default', db: Session = Depends(get_db)):
    spots = crud.get_spots(db=db, plan_id=plan_id)
    return spots

@app.get("/memo", response_model=List[schemas.MemoRes])
async def get_memos(spot_id: int = 0, db: Session = Depends(get_db)):
    memos = crud.get_memos(db=db, spot_id=spot_id)
    return memos


# POST
@app.post("/plan", response_model=Union[schemas.PlanRes,  Literal[False]])
async def create_plan(plan: schemas.PlanReq, db: Session = Depends(get_db)):
    new_plan = crud.create_plan(db=db, plan=plan)
    return new_plan

@app.post("/spot", response_model=Union[schemas.SpotRes,  Literal[False]])
async def create_spot(spot: schemas.SpotReq, db: Session = Depends(get_db)):
    new_spot = crud.create_spot(db=db, spot=spot)
    return new_spot

@app.post("/memo", response_model=Union[schemas.MemoRes,  Literal[False]])
async def create_memo(memo: schemas.MemoReq, db: Session = Depends(get_db)):
    new_memo = crud.create_memo(db=db, memo=memo)
    return new_memo
