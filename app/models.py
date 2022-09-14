from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .database import Base

class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(String, primary_key=True, index=True)
    verify_key = Column(String, nullable=False)
    plan_name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)


class Spot(Base):
    __tablename__ = 'spots'
    plan_id = Column(String, ForeignKey('plans.plan_id', ondelete='CASCADE'))
    spot_id = Column(Integer, primary_key=True, index=True)
    spot_name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    image = Column(String, nullable=False)
    priority = Column(Boolean, nullable=False)


class Memo(Base):
    __tablename__ = 'memos'
    plan_id = Column(String, ForeignKey('plans.plan_id', ondelete='CASCADE'))
    spot_id = Column(Integer, ForeignKey('spots.spot_id', ondelete='CASCADE'))
    memo_id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    marked = Column(String, nullable=False)
