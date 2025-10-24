from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class PsychTest(Base):
    __tablename__ = "psych_tests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_type = Column(String(32), nullable=False)  # PHQ9/GAD7/PSS14/PANAS/ECR36/IRI28/RSES/SCS26/MBI22/PCL5_20
    answers_json = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)  # 主要分数（可能是总分或平均分）
    result_json = Column(Text, nullable=True)  # 存储完整结果（包括分量表分数、等级、建议等）
    ai_report = Column(Text, nullable=True)  # AI 生成的专业评估报告
    date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 