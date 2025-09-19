from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class PsychTest(Base):
    __tablename__ = "psych_tests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_type = Column(String(32), nullable=False)  # PHQ9/GAD7
    answers_json = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now()) 