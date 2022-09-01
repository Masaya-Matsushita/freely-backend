import os
import hashlib
from sqlalchemy.orm import Session
from . import models, schemas
from dotenv import load_dotenv

load_dotenv()

# プラン一覧取得
def get_plans(db: Session, planId: str):
    return db.query(models.Plan).filter(models.Plan.plan_id==planId).all()[0]

# スポット一覧取得
def get_spots(db: Session, planId: str):
    return db.query(models.Spot).filter(models.Spot.plan_id==planId).all()

# メモ一覧取得
def get_memos(db: Session):
    return db.query(models.Memo).all()

# パスワード認証
def auth_user(db: Session, auth: schemas.Auth):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==auth.plan_id).all()[0]
    key = auth.password + os.environ['SALT']
    hash_key = hashlib.sha256(key.encode()).hexdigest()
    if plan.verify_key == hash_key:
        return True
    else:
        return False

# プラン登録
# idはサーバー側
def create_plan(db: Session, plan: schemas.Plan):
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

# スポット登録
def create_spot(db: Session, spot: schemas.Spot):
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

# メモ登録
def create_memo(db: Session, memo: schemas.Memo):
    db_memo = models.Memo(
        spot_id = memo.spot_id,
        text = memo.text,
        marked = memo.marked,
    )
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
