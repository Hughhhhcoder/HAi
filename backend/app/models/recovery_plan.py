from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class RecoveryPlan(Base):
    __tablename__ = "recovery_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_text = Column(Text, nullable=False)
    stage = Column(String(32), nullable=True)  # 阶段，如"第一周"
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 