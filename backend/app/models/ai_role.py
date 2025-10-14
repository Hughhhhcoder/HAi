from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class AIRole(Base):
    __tablename__ = "ai_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(32), unique=True, nullable=False)
    prompt_template = Column(String(1024), nullable=False)
    
    # 关联到知识库（多对多，延迟导入避免循环依赖）
    knowledge_base = relationship(
        "PsychologyKnowledge",
        secondary="role_knowledge_mapping",
        back_populates="roles"
    ) 