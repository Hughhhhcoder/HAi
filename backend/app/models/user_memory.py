"""
用户长期记忆模型 - 让 AI 角色逐渐了解用户
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class UserMemory(Base):
    """
    用户画像/长期记忆表
    存储 AI 在长期交互中学到的用户信息
    """
    __tablename__ = "user_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("ai_roles.id"), nullable=True)  # None 表示通用记忆
    
    # 记忆类型：personality, preference, concern, goal, trigger, resource 等
    memory_type = Column(String(32), nullable=False, index=True)
    
    # 记忆内容（简短摘要）
    content = Column(Text, nullable=False)
    
    # 重要性评分 1-10
    importance = Column(Integer, default=5)
    
    # 最后更新时间（用于记忆衰减）
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 访问次数（频繁被引用的记忆更重要）
    access_count = Column(Integer, default=0)


class UserInsight(Base):
    """
    用户深层洞察表
    AI 对用户的综合分析和理解
    """
    __tablename__ = "user_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # 核心特质（JSON 字符串，包含性格、价值观等）
    core_traits = Column(Text, nullable=True)
    
    # 主要困扰/目标
    main_concerns = Column(Text, nullable=True)
    
    # 优势和资源
    strengths = Column(Text, nullable=True)
    
    # 应对模式
    coping_patterns = Column(Text, nullable=True)
    
    # 触发因素
    triggers = Column(Text, nullable=True)
    
    # 综合摘要（AI 生成）
    summary = Column(Text, nullable=True)
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

