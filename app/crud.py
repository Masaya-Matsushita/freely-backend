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
    plan_list = db.query(models.Plan).all()
    return plan_list

def get_spot_test(db: Session):
    spot_list = db.query(models.Spot).all()
    return spot_list

def get_memo_test(db: Session):
    memo_list = db.query(models.Memo).all()
    return memo_list


# プラン取得
# TODO: planIdの値が誤っているとき、500エラーが返る -> undefinedを返すのが綺麗？
def get_plan(db: Session, plan_id: str):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).all()[0]
    return {
        'plan_name': plan.plan_name,
        'start_date': plan.start_date,
        'end_date': plan.end_date,
    }


# スポット取得
# TODO: spotIdの値が誤っているとき、500エラーが返る -> undefinedを返すのが綺麗？
def get_spot(db: Session, plan_id: str, spot_id: str):
    spot = db.query(models.Spot).filter(models.Spot.spot_id==int(spot_id)).all()[0]
    if spot.plan_id == plan_id:
        return {
            'spot_name': spot.spot_name,
            'icon': spot.icon,
            'image': spot.image
        }


# スポット一覧取得
def get_spot_list(db: Session, plan_id: str):
    return db.query(models.Spot).filter(models.Spot.plan_id==plan_id).all()


# メモ一覧取得
def get_memo_list(db: Session, plan_id: str, spot_id: str):
    memo_list = db.query(models.Memo).filter(models.Memo.spot_id==int(spot_id)).all()
    # plan_idが正しくないリクエストを規制
    if memo_list and memo_list[0].plan_id != plan_id:
        return False
    else:
        return memo_list


# プラン登録
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
    # パスワードがあれば認証
    if spot.password:
        isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    else:
        return False

    # 認証成功でデータベースに追加
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
    # パスワードがあれば認証
    if memo.password:
        isAuth = auth_user(db=db, plan_id=memo.plan_id, password=memo.password)
    else:
        return False

    # 認証成功でデータベースに追加
    if isAuth:
        db_memo = models.Memo(
            plan_id = memo.plan_id,
            spot_id = memo.spot_id,
            text = memo.text,
            marked = memo.marked,
        )
        db.add(db_memo)
        db.commit()
        db.refresh(db_memo)
        return True
    return False
