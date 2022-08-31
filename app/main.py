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
@app.get("/plan", response_model=schemas.Plan)
async def read_plan(db: Session = Depends(get_db)):
    plan = crud.get_plan(db)
    return plan

@app.get("/spot", response_model=schemas.Spot)
async def read_spot(db: Session = Depends(get_db)):
    spot = crud.get_spot(db)
    return spot

@app.get("/memo", response_model=schemas.Memo)
async def read_memo(db: Session = Depends(get_db)):
    memo = crud.get_memo(db)
    return memo


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
