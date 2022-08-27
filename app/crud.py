from sqlalchemy.orm import Session
from . import models, schemas

# プラン一覧取得
def get_plans(db: Session):
    return db.query(models.Plan).all()

# スポット一覧取得
def get_spots(db: Session):
    return db.query(models.Spot).all()

# メモ一覧取得
def get_memos(db: Session):
    return db.query(models.Memo).all()

# プラン登録
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

# TODO: 各データ追加処理において主キーは指定すべきか
# NOTE: フロントから自動生成した一意の値を渡す？
# NOTE: 指定しない場合、連番が自動で割り振られた

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
