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
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).first()
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
def get_plan(db: Session, plan_id: str):
    plan = db.query(models.Plan).filter(models.Plan.plan_id==plan_id).first()
    if plan:
        return [{
            'plan_name': plan.plan_name,
            'start_date': plan.start_date,
            'end_date': plan.end_date,
        }]
    else:
        return None


# スポット取得
def get_spot(db: Session, plan_id: str, spot_id: str):
    spot = db.query(models.Spot).filter(models.Spot.spot_id==int(spot_id)).first()
    # plan_idが正しいとき
    if spot and spot.plan_id == plan_id:
        return [{
            'spot_name': spot.spot_name,
            'icon': spot.icon,
            'image': spot.image
        }]
    else:
        return None


# スポット一覧取得
def get_spot_list(db: Session, plan_id: str):
    return db.query(models.Spot).filter(models.Spot.plan_id==plan_id).all()


# メモ一覧取得
def get_memo_list(db: Session, plan_id: str, spot_id: str):
    memo_list = db.query(models.Memo).filter(models.Memo.spot_id==int(spot_id)).all()
    # 空のとき
    if memo_list and len(memo_list) == 0:
        return memo_list
    # plan_idが正しいとき
    elif memo_list and memo_list[0].plan_id == plan_id:
        return memo_list
    else:
        return None


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


# プラン更新
def update_plan(db: Session, plan: schemas.PlanReqPut):
    # パスワードがあれば認証
    if plan.password:
        isAuth = auth_user(db=db, plan_id=plan.plan_id, password=plan.password)
    else:
        return False

    # 認証成功でデータを更新
    if isAuth:
        db_plan = db.query(models.Plan).filter(models.Plan.plan_id==plan.plan_id).first()
        db_plan.plan_name = plan.plan_name
        db_plan.start_date = plan.start_date
        db_plan.end_date = plan.end_date
        db.commit()
        db.refresh(db_plan)
        return True
    return False


# スポット更新
def update_spot(db: Session, spot: schemas.SpotReqPutBody):
    # パスワードがあれば認証
    if spot.password:
        isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    else:
        return False

    # 認証成功でデータを更新
    if isAuth:
        db_spot = db.query(models.Spot).filter(models.Spot.spot_id==spot.spot_id).first()
        db_spot.spot_name = spot.spot_name
        db_spot.icon = spot.icon
        db_spot.image = spot.image
        db.commit()
        db.refresh(db_spot)
        return True
    return False


# priority更新
def update_priority(db: Session, spot: schemas.SpotReqPutPriority):
    # パスワードがあれば認証
    if spot.password:
        isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    else:
        return False

    # 認証成功でpriority更新
    if isAuth:
        db_spot = db.query(models.Spot).filter(models.Spot.spot_id==spot.spot_id).first()
        db_spot.priority = spot.priority
        db.commit()
        db.refresh(db_spot)
        return True
    return False


# スポット削除
def delete_spot(db: Session, spot: schemas.SpotReqDelete):
    # パスワードがあれば認証
    if spot.password:
        isAuth = auth_user(db=db, plan_id=spot.plan_id, password=spot.password)
    else:
        return False

    # 認証成功でデータを削除
    if isAuth:
        db.query(models.Spot).filter(models.Spot.spot_id==spot.spot_id).delete()
        db.commit()
        return True
    return False


# メモ削除
def delete_memo(db: Session, memo: schemas.MemoReqDelete):
    # パスワードがあれば認証
    if memo.password:
        isAuth = auth_user(db=db, plan_id=memo.plan_id, password=memo.password)
    else:
        return False

    # 認証成功でデータを削除
    if isAuth:
        db.query(models.Memo).filter(models.Memo.memo_id==memo.memo_id).delete()
        db.commit()
        return True
    return False
