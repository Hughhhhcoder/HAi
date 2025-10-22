from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class AIRole(Base):
    __tablename__ = "ai_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(32), unique=True, nullable=False)
    prompt_template = Column(Text, nullable=False)  # 改为 TEXT 类型以支持更长的专业提示词 