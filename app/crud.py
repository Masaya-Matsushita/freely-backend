import os
import hashlib
from sqlalchemy.orm import Session
from . import models, schemas
from dotenv import load_dotenv


load_dotenv()


# パスワード認証
def auth_user(db: Session, plan_id: str, password: str):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).all()[0]
    key = password + os.environ['SALT']
    hash_key = hashlib.sha256(key.encode()).hexdigest()
    if plan.verify_key == hash_key:
        return True
    else:
        return False


# プラン取得
def get_plan(db: Session, plan_id: str):
    return db.query(models.Plan).filter(models.Plan.plan_id==plan_id).all()[0]

# スポット一覧取得
def get_spots(db: Session, plan_id: str):
    return db.query(models.Spot).filter(models.Spot.plan_id==plan_id).all()

# メモ一覧取得
def get_memos(db: Session, spot_id: int):
    return db.query(models.Memo).filter(models.Memo.spot_id==spot_id).all()


# プラン登録
# TODO: idはサーバー側
def create_plan(db: Session, plan: schemas.PlanReq):
    isAuth = auth_user(db=db, plan_id=plan.plan_id, password=plan.password)
    if isAuth:
        db_plan = models.Plan(
            plan_id = plan.plan_id,
            plan_name = plan.plan_name,
            start_date = plan.start_date,
            end_date = plan.end_date,
            verify_key = plan.verify_key,
            email = plan.email,
            timestamp = plan.timestamp
        )
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan
    return False

# スポット登録
def create_spot(db: Session, spot: schemas.SpotReq):
    isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    if isAuth:
        db_spot = models.Spot(
            plan_id = spot.plan_id,
            spot_name = spot.spot_name,
            image = spot.image,
            url =  spot.url,
            priority = spot.priority,
            visited = spot.visited,
            icon = spot.icon
        )
        db.add(db_spot)
        db.commit()
        db.refresh(db_spot)
        return db_spot
    return False

# メモ登録
def create_memo(db: Session, memo: schemas.MemoReq):
    isAuth = auth_user(db=db, plan_id=memo.plan_id, password=memo.password)
    if isAuth:
        db_memo = models.Memo(
            spot_id = memo.spot_id,
            text = memo.text,
            marked = memo.marked,
        )
        db.add(db_memo)
        db.commit()
        db.refresh(db_memo)
        return db_memo
    return False
