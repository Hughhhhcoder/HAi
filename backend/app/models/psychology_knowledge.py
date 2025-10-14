"""
心理学专业知识库模型
用于存储各类心理学理论、技术、案例等专业知识
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# 角色与知识的多对多关系表
role_knowledge_association = Table(
    'role_knowledge_mapping',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('ai_roles.id'), primary_key=True),
    Column('knowledge_id', Integer, ForeignKey('psychology_knowledge.id'), primary_key=True),
    Column('priority', Integer, default=5)  # 1-10, 该知识对该角色的重要性
)

class PsychologyKnowledge(Base):
    """心理学专业知识库"""
    __tablename__ = "psychology_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)  # 知识标题
    category = Column(String(100), nullable=False, index=True)  # 分类：theory/technique/case/symptom/intervention
    subcategory = Column(String(100))  # 子分类：如 CBT/psychodynamic/humanistic
    content = Column(Text, nullable=False)  # 知识内容（详细描述）
    keywords = Column(Text)  # 关键词，逗号分隔，用于检索
    source = Column(String(500))  # 来源（文献、书籍等）
    reliability_score = Column(Integer, default=8)  # 可靠性评分 1-10
    usage_count = Column(Integer, default=0)  # 被使用次数
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关联到多个角色（多对多）
    roles = relationship(
        "AIRole",
        secondary=role_knowledge_association,
        back_populates="knowledge_base"
    )
    
    def __repr__(self):
        return f"<PsychologyKnowledge(id={self.id}, title='{self.title}', category='{self.category}')>"


class KnowledgeUsageLog(Base):
    """知识使用日志 - 记录哪些知识在哪次对话中被使用"""
    __tablename__ = "knowledge_usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    knowledge_id = Column(Integer, ForeignKey("psychology_knowledge.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("ai_roles.id"), nullable=False)
    relevance_score = Column(Float)  # 检索时的相关性得分
    created_at = Column(DateTime, default=func.now())
    
    conversation = relationship("Conversation")
    knowledge = relationship("PsychologyKnowledge")
    user = relationship("User")
    ai_role = relationship("AIRole")
    
    def __repr__(self):
        return f"<KnowledgeUsageLog(conv_id={self.conversation_id}, knowledge_id={self.knowledge_id})>"

