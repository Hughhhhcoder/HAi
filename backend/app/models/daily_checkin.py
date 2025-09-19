from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from app.core.database import Base

class DailyCheckin(Base):
    __tablename__ = "daily_checkin"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    mood = Column(String(32), nullable=True)
    sleep_hours = Column(Float, nullable=True)
    completed_tasks = Column(String(256), nullable=True)  # 逗号分隔 