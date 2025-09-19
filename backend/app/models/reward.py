from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False, default=0)
    reward_history = Column(String(256), nullable=True)  # 逗号分隔
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 