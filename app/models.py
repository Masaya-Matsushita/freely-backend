from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from .database import Base


# ソルトはどこに保存すべきか
class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(String, primary_key=True, index=True)
    plan_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    verify_key = Column(String, nullable=False)
    email = Column(String)
    timestamp = Column(Date, nullable=False)


class Spot(Base):
    __tablename__ = 'spots'
    spot_id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(String, ForeignKey('plans.plan_id', ondelete='CASCADE'))
    spot_name = Column(String, nullable=False)
    image = Column(String)
    url = Column(String)
    priority = Column(Boolean, nullable=False)
    visited = Column(Boolean, nullable=False)
    icon = Column(Integer)
    

class Memo(Base):
    __tablename__ = 'memos'
    memo_id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(String, ForeignKey('spots.spot_id', ondelete='CASCADE'))
    text = Column(String, nullable=False)
    marked = Column(String, nullable=False)
