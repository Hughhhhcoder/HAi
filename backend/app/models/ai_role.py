from sqlalchemy import Column, Integer, String
from app.core.database import Base

class AIRole(Base):
    __tablename__ = "ai_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(32), unique=True, nullable=False)
    prompt_template = Column(String(1024), nullable=False) 