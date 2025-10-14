"""
专业知识检索与管理服务
为 AI 对话提供专业心理学知识支持
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.psychology_knowledge import PsychologyKnowledge, KnowledgeUsageLog, role_knowledge_association
from typing import List, Optional
import re


def retrieve_knowledge_for_conversation(
    db: Session,
    role_id: int,
    user_message: str,
    user_concerns: List[str] = None,
    top_k: int = 3
) -> List[PsychologyKnowledge]:
    """
    为对话检索相关的专业知识
    
    Args:
        db: 数据库会话
        role_id: AI 角色 ID
        user_message: 用户消息内容
        user_concerns: 用户的困扰列表（从 user_memory 提取）
        top_k: 返回最相关的前 k 条知识
    
    Returns:
        相关知识列表
    """
    # 提取用户消息中的关键词
    message_keywords = extract_keywords_from_message(user_message)
    
    # 合并用户困扰作为额外关键词
    if user_concerns:
        message_keywords.extend(user_concerns)
    
    # 1. 优先检索该角色专属知识
    role_specific_knowledge = db.query(PsychologyKnowledge)\
        .join(role_knowledge_association)\
        .filter(role_knowledge_association.c.role_id == role_id)\
        .order_by(role_knowledge_association.c.priority.desc())\
        .limit(top_k).all()
    
    # 2. 基于关键词检索通用知识
    if message_keywords:
        keyword_conditions = [
            or_(
                PsychologyKnowledge.title.contains(kw),
                PsychologyKnowledge.content.contains(kw),
                PsychologyKnowledge.keywords.contains(kw)
            )
            for kw in message_keywords[:5]  # 取前5个关键词
        ]
        
        general_knowledge = db.query(PsychologyKnowledge)\
            .filter(or_(*keyword_conditions))\
            .order_by(PsychologyKnowledge.reliability_score.desc())\
            .limit(top_k).all()
    else:
        general_knowledge = []
    
    # 3. 合并并去重
    all_knowledge = role_specific_knowledge + general_knowledge
    unique_knowledge = list({k.id: k for k in all_knowledge}.values())
    
    # 4. 按相关性和可靠性排序，返回 top_k
    unique_knowledge.sort(key=lambda k: k.reliability_score, reverse=True)
    return unique_knowledge[:top_k]


def extract_keywords_from_message(message: str) -> List[str]:
    """
    从用户消息中提取心理学相关关键词
    """
    # 常见心理学关键词库
    psychology_keywords = [
        "焦虑", "抑郁", "压力", "失眠", "恐惧", "强迫", "创伤", "悲伤",
        "愤怒", "孤独", "自卑", "完美主义", "拖延", "人际关系", "亲密关系",
        "工作", "学业", "家庭", "情绪", "心情", "痛苦", "困扰", "迷茫",
        "自我", "意义", "目标", "动力", "疲惫", "倦怠", "紧张", "不安",
        "难过", "委屈", "无助", "绝望", "空虚", "麻木", "敏感", "多疑",
        "社交", "沟通", "冲突", "分手", "离婚", "丧失", "哀伤", "思念",
        "童年", "原生家庭", "父母", "孩子", "婚姻", "恋爱", "友情",
        "自信", "自尊", "身份", "价值", "成就", "失败", "挫折", "困难"
    ]
    
    # 提取消息中出现的关键词
    keywords = []
    for kw in psychology_keywords:
        if kw in message:
            keywords.append(kw)
    
    return keywords


def format_knowledge_for_prompt(knowledge_list: List[PsychologyKnowledge]) -> str:
    """
    将检索到的知识格式化为适合注入 prompt 的文本
    """
    if not knowledge_list:
        return ""
    
    formatted = "【专业知识参考】\n"
    for idx, k in enumerate(knowledge_list, 1):
        formatted += f"{idx}. {k.title} ({k.category})\n"
        formatted += f"   {k.content}\n"
        if k.source:
            formatted += f"   来源: {k.source}\n"
        formatted += "\n"
    
    formatted += "请基于以上专业知识，结合你的角色定位，为用户提供专业、准确的回复。\n"
    return formatted


def log_knowledge_usage(
    db: Session,
    conversation_id: int,
    knowledge_ids: List[int],
    user_id: int,
    role_id: int
):
    """
    记录知识使用情况
    """
    for kid in knowledge_ids:
        usage_log = KnowledgeUsageLog(
            conversation_id=conversation_id,
            knowledge_id=kid,
            user_id=user_id,
            role_id=role_id
        )
        db.add(usage_log)
        
        # 更新知识使用次数
        knowledge = db.query(PsychologyKnowledge).filter(PsychologyKnowledge.id == kid).first()
        if knowledge:
            knowledge.usage_count += 1
    
    db.commit()


def add_knowledge(
    db: Session,
    title: str,
    category: str,
    content: str,
    subcategory: str = None,
    keywords: str = None,
    source: str = None,
    reliability_score: int = 8
) -> PsychologyKnowledge:
    """
    添加专业知识
    """
    knowledge = PsychologyKnowledge(
        title=title,
        category=category,
        subcategory=subcategory,
        content=content,
        keywords=keywords,
        source=source,
        reliability_score=reliability_score
    )
    db.add(knowledge)
    db.commit()
    db.refresh(knowledge)
    return knowledge


def link_knowledge_to_role(
    db: Session,
    knowledge_id: int,
    role_id: int,
    priority: int = 5
):
    """
    将知识关联到特定角色
    """
    # 使用原生 SQL 插入关联
    from sqlalchemy import text
    stmt = text(
        "INSERT INTO role_knowledge_mapping (role_id, knowledge_id, priority) "
        "VALUES (:role_id, :knowledge_id, :priority) "
        "ON DUPLICATE KEY UPDATE priority = :priority"
    )
    db.execute(stmt, {"role_id": role_id, "knowledge_id": knowledge_id, "priority": priority})
    db.commit()

