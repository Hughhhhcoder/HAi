from sqlalchemy import Column, Integer, String, ForeignKey, Time
from app.core.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    sleep_time = Column(String(8), nullable=True)  # HH:MM
    wake_time = Column(String(8), nullable=True)   # HH:MM
    preferences = Column(String(256), nullable=True)  # JSON字符串或逗号分隔 