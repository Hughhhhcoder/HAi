from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class AIRole(Base):
    __tablename__ = "ai_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(32), unique=True, nullable=False)
    description = Column(Text, nullable=True)  # 用户可见的描述
    emoji = Column(String(10), nullable=True)  # 角色图标
    tags = Column(String(255), nullable=True)  # 标签，逗号分隔
    gradient = Column(String(100), nullable=True)  # 渐变色彩
    prompt_template = Column(Text, nullable=False)  # 内部提示词，用户不可见 