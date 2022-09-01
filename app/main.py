from typing import List
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

# Read
@app.get("/plan", response_model=List[schemas.Plan])
async def read_plans(planId: str = 'default', db: Session = Depends(get_db)):
    plans = crud.get_plans(db=db, planId=planId)
    return plans

@app.get("/spot", response_model=List[schemas.Spot])
async def read_spots(planId: str = 'default' ,db: Session = Depends(get_db)):
    spots = crud.get_spots(db=db, planId=planId)
    return spots

@app.get("/memo", response_model=schemas.Memo)
async def read_memos(db: Session = Depends(get_db)):
    memos = crud.get_memos(db)
    return memos


# Create
@app.post("/plan", response_model=schemas.Plan)
async def create_plan(plan: schemas.Plan, db: Session = Depends(get_db)):
    new_plan = crud.create_plan(db=db, plan=plan)
    return new_plan

@app.post("/spot", response_model=schemas.Spot)
async def create_spot(spot: schemas.Spot, db: Session = Depends(get_db)):
    new_spot = crud.create_spot(db=db, spot=spot)
    return new_spot

@app.post("/memo", response_model=schemas.Memo)
async def create_memo(memo: schemas.Memo, db: Session = Depends(get_db)):
    new_memo = crud.create_memo(db=db, memo=memo)
    return new_memo
