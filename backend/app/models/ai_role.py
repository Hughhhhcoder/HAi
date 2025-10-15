from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class AIRole(Base):
    __tablename__ = "ai_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(32), unique=True, nullable=False)
    prompt_template = Column(Text, nullable=False)  # 改为 TEXT 类型以支持更长的专业提示词
    
    # 关联到知识库（多对多，延迟导入避免循环依赖）
    knowledge_base = relationship(
        "PsychologyKnowledge",
        secondary="role_knowledge_mapping",
        back_populates="roles"
    ) 