from typing import List
from fastapi import FastAPI, Depends, HTTPException
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

# 404エラーを発行
def raise_404_exception(item: str):
    raise HTTPException(status_code=404, detail=f'{item} not found')


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
@app.get("/plan", response_model=List[schemas.PlanResGet])
def get_plan(plan_id: str = 'default', db: Session = Depends(get_db)):
    res_plan = crud.get_plan(db=db, plan_id=plan_id)
    if res_plan is None:
        raise_404_exception('Plan')
    return res_plan

@app.get("/spot", response_model=List[schemas.SpotResGet])
def get_spot(plan_id: str = 'default', spot_id: str = '0', db: Session = Depends(get_db)):
    res_spot = crud.get_spot(db=db, plan_id=plan_id, spot_id=spot_id)
    if res_spot is None:
        raise_404_exception('Spot')
    return res_spot

@app.get("/spot-list", response_model=List[schemas.SpotListResGet])
def get_spot_list(plan_id: str = 'default', db: Session = Depends(get_db)):
    res_spot_list = crud.get_spot_list(db=db, plan_id=plan_id)
    if res_spot_list is None:
        raise_404_exception('Spot')
    return res_spot_list

@app.get("/memo-list", response_model=List[schemas.MemoListResGet])
def get_memo_list(plan_id: str = 'default', spot_id: str = '0', db: Session = Depends(get_db)):
    res_memo = crud.get_memo_list(db=db, plan_id=plan_id, spot_id=spot_id)
    if res_memo is None:
        raise_404_exception('Memo')
    return res_memo


# POST
@app.post("/auth", response_model=bool)
def auth_user(auth: schemas.AuthUser, db: Session = Depends(get_db)):
    res_auth = crud.auth_user(db=db, plan_id=auth.plan_id, password=auth.password)
    if res_auth is None:
        raise_404_exception('Plan')
    return res_auth

@app.post("/plan", response_model=schemas.PlanResPost)
def create_plan(plan: schemas.PlanReqPost, db: Session = Depends(get_db)):
    res_plan = crud.create_plan(db=db, plan=plan)
    return res_plan

@app.post("/spot", response_model=bool)
def create_spot(spot: schemas.SpotReqPost, db: Session = Depends(get_db)):
    res_spot = crud.create_spot(db=db, spot=spot)
    if res_spot is None:
        raise_404_exception('Plan')
    return res_spot

@app.post("/memo", response_model=bool)
def create_memo(memo: schemas.MemoReqPost, db: Session = Depends(get_db)):
    res_memo = crud.create_memo(db=db, memo=memo)
    if res_memo is None:
        raise_404_exception('Plan')
    return res_memo


#PUT
@app.put("/plan", response_model=bool)
def update_plan(plan: schemas.PlanReqPut, db: Session = Depends(get_db)):
    res_plan = crud.update_plan(db=db, plan=plan)
    return res_plan

@app.put("/spot", response_model=bool)
def update_spot(spot: schemas.SpotReqPutBody, db: Session = Depends(get_db)):
    res_spot = crud.update_spot(db=db, spot=spot)
    return res_spot

@app.put("/priority", response_model=bool)
def update_priority(spot: schemas.SpotReqPutPriority, db: Session = Depends(get_db)):
    res_priority = crud.update_priority(db=db, spot=spot)
    return res_priority


# DELETE
@app.delete("/spot", response_model=bool)
def delete_spot(spot: schemas.SpotReqDelete, db: Session = Depends(get_db)):
    res_spot = crud.delete_spot(db=db, spot=spot)
    return res_spot

@app.delete("/memo", response_model=bool)
def delete_memo(memo: schemas.MemoReqDelete, db: Session = Depends(get_db)):
    res_memo = crud.delete_memo(db=db, memo=memo)
    return res_memo
