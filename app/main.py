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

@app.post("/test-plans")
async def plans(plans: schemas.Plan):
    return {"plans": plans}

@app.post("/test-spots")
async def spots(spots: schemas.Spot):
    return {"spots": spots}

@app.post("/test-memos")
async def memos(memos: schemas.Memo):
    return {"memos": memos}


# Read
@app.get("/plans", response_model=List[schemas.Plan])
async def read_plans(db: Session = Depends(get_db)):
    plans = crud.get_plans(db)
    return plans

@app.get("/spots", response_model=List[schemas.Spot])
async def read_spots(db: Session = Depends(get_db)):
    spots = crud.get_spots(db)
    return spots

@app.get("/memos", response_model=List[schemas.Memo])
async def read_memos(db: Session = Depends(get_db)):
    memos = crud.get_memos(db)
    return memos


# Create
@app.post("/plans", response_model=schemas.Plan)
async def create_plan(plan: schemas.Plan, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)

@app.post("/spots", response_model=schemas.Spot)
async def create_spot(spot: schemas.Spot, db: Session = Depends(get_db)):
    return crud.create_spot(db=db, spot=spot)

@app.post("/memos", response_model=schemas.Memo)
async def create_memo(memo: schemas.Memo, db: Session = Depends(get_db)):
    return crud.create_memo(db=db, memo=memo)
