from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# https://fastapi.tiangolo.com/ja/tutorial/dependencies/dependencies-with-yield/
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# test
@app.get("/plan-test", response_model=List[schemas.PlanTest])
def get_plan_test(db: Session = Depends(get_db)):
    return crud.get_plan_test(db=db)

@app.get("/spot-test", response_model=List[schemas.SpotTest])
def get_spot_test(db: Session = Depends(get_db)):
    return crud.get_spot_test(db=db)

@app.get("/memo-test", response_model=List[schemas.MemoTest])
def get_memo_test(db: Session = Depends(get_db)):
    return crud.get_memo_test(db=db)


# GET
@app.get("/plan", response_model=schemas.PlanResGet)
def get_plan(plan_id: str = 'default', db: Session = Depends(get_db)):
    return crud.get_plan(db=db, plan_id=plan_id)

@app.get("/spot", response_model=List[schemas.SpotResGet])
def get_spots(plan_id: str = 'default', db: Session = Depends(get_db)):
    return crud.get_spots(db=db, plan_id=plan_id)

@app.get("/memo", response_model=List[schemas.MemoResGet])
def get_memos(spot_id: int = 0, db: Session = Depends(get_db)):
    return crud.get_memos(db=db, spot_id=spot_id)


# POST
@app.post("/auth", response_model=bool)
def auth_user(auth: schemas.AuthUser, db: Session = Depends(get_db)):
    return crud.auth_user(db=db, plan_id=auth.plan_id, password=auth.password)

@app.post("/plan", response_model=schemas.PlanResPost)
def create_plan(plan: schemas.PlanReqPost, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)

@app.post("/spot", response_model=bool)
def create_spot(spot: schemas.SpotReqPost, db: Session = Depends(get_db)):
    return crud.create_spot(db=db, spot=spot)

@app.post("/memo", response_model=bool)
def create_memo(memo: schemas.MemoReqPost, db: Session = Depends(get_db)):
    return crud.create_memo(db=db, memo=memo)
