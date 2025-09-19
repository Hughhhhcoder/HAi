from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("ai_roles.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_user = Column(Boolean, default=True)  # True 表示用户消息，False 表示 AI 回复
    image_url = Column(String(256), nullable=True)  # 图片消息
    audio_url = Column(String(256), nullable=True)  # 新增，语音消息
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 