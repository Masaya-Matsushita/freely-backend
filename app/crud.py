import os
import hashlib
import uuid
from sqlalchemy.orm import Session
from . import models, schemas
from dotenv import load_dotenv


load_dotenv()


# saltを追加しハッシュ化
def get_hash(text: str):
    key = text + os.environ['SALT']
    return hashlib.sha256(key.encode()).hexdigest()


# パスワード認証
def auth_user(db: Session, plan_id: str, password: str):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).all()[0]
    hash_key = get_hash(password)
    if plan.verify_key == hash_key:
        return True
    else:
        return False


# テスト用
def get_plan_test(db: Session):
    plans = db.query(models.Plan).all()
    return plans

def get_spot_test(db: Session):
    spots = db.query(models.Spot).all()
    return spots

def get_memo_test(db: Session):
    memos = db.query(models.Memo).all()
    return memos


# プラン取得
def get_plan(db: Session, plan_id: str):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).all()[0]
    return {
        'plan_name': plan.plan_name,
        'start_date': plan.start_date,
        'end_date': plan.end_date,
    }

# スポット一覧取得
def get_spots(db: Session, plan_id: str):
    return db.query(models.Spot).filter(models.Spot.plan_id==plan_id).all()

# メモ一覧取得
def get_memos(db: Session, spot_id: int):
    return db.query(models.Memo).filter(models.Memo.spot_id==spot_id).all()


# プラン登録
# TODO: idはサーバー側
def create_plan(db: Session, plan: schemas.PlanReqPost):
    db_plan = models.Plan(
        plan_id = str(uuid.uuid4()),
        plan_name = plan.plan_name,
        start_date = plan.start_date,
        end_date = plan.end_date,
        verify_key = get_hash(plan.password),
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return { 'plan_id' : db_plan.plan_id }

# スポット登録
def create_spot(db: Session, spot: schemas.SpotReqPost):
    isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    if isAuth:
        db_spot = models.Spot(
            plan_id = spot.plan_id,
            spot_name = spot.spot_name,
            image = spot.image,
            icon = spot.icon,
            priority = False,
            visited = False,
        )
        db.add(db_spot)
        db.commit()
        db.refresh(db_spot)
        return True
    return False

# メモ登録
def create_memo(db: Session, memo: schemas.MemoReqPost):
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
        return True
    return False
