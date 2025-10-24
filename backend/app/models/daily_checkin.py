from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class DailyCheckin(Base):
    __tablename__ = "daily_checkin"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    mood = Column(String(32), nullable=True)
    sleep_hours = Column(Float, nullable=True)
    completed_tasks = Column(String(256), nullable=True)  # 逗号分隔
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 