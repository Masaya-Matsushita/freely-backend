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


# GET
@app.get("/history", response_model=schemas.PlanResHistory)
async def get_history(plan_id: str = 'default', db: Session = Depends(get_db)):
    return crud.get_history(db=db, plan_id=plan_id)

@app.get("/plan", response_model=schemas.PlanResGet)
async def get_plan(plan_id: str = 'default', db: Session = Depends(get_db)):
    return crud.get_plan(db=db, plan_id=plan_id)

@app.get("/spot", response_model=List[schemas.SpotResGet])
async def get_spots(plan_id: str = 'default', db: Session = Depends(get_db)):
    return crud.get_spots(db=db, plan_id=plan_id)

@app.get("/memo", response_model=List[schemas.MemoResGet])
async def get_memos(spot_id: int = 0, db: Session = Depends(get_db)):
    return crud.get_memos(db=db, spot_id=spot_id)


# POST
@app.post("/plan", response_model=schemas.PlanResPost)
async def create_plan(plan: schemas.PlanReqPost, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)

@app.post("/spot", response_model=bool)
async def create_spot(spot: schemas.SpotReqPost, db: Session = Depends(get_db)):
    return crud.create_spot(db=db, spot=spot)

@app.post("/memo", response_model=bool)
async def create_memo(memo: schemas.MemoReqPost, db: Session = Depends(get_db)):
    return crud.create_memo(db=db, memo=memo)
