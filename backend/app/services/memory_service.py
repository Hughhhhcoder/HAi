"""
用户记忆和画像服务
让 AI 角色通过长期交互逐渐了解用户
"""
from sqlalchemy.orm import Session
from app.models.user_memory import UserMemory, UserInsight
from app.models.user_profile import UserProfile
from app.models.psych_test import PsychTest
from app.models.daily_checkin import DailyCheckin
import json
from datetime import datetime, timedelta


def get_user_profile_summary(db: Session, user_id: int) -> str:
    """
    生成用户画像摘要，供 AI 理解用户背景
    """
    parts = []
    
    # 1. 基础作息信息
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        if profile.sleep_time and profile.wake_time:
            parts.append(f"作息：{profile.wake_time}起床，{profile.sleep_time}睡觉")
        if profile.preferences:
            parts.append(f"偏好：{profile.preferences}")
    
    # 2. 最近的心理测评结果
    recent_tests = db.query(PsychTest)\
        .filter(PsychTest.user_id == user_id)\
        .order_by(PsychTest.date.desc())\
        .limit(2)\
        .all()
    
    if recent_tests:
        test_summary = []
        for test in recent_tests:
            test_summary.append(f"{test.test_type}={test.score}分")
        parts.append(f"近期测评：{', '.join(test_summary)}")
    
    # 3. 最近打卡情况（反映状态）
    recent_checkins = db.query(DailyCheckin)\
        .filter(DailyCheckin.user_id == user_id)\
        .order_by(DailyCheckin.date.desc())\
        .limit(7)\
        .all()
    
    if recent_checkins:
        moods = [c.mood for c in recent_checkins if c.mood]
        if moods:
            parts.append(f"近期心情：{', '.join(moods[:3])}")
    
    # 4. 深层洞察（如果有）
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    if insight:
        if insight.main_concerns:
            parts.append(f"主要困扰：{insight.main_concerns}")
        if insight.strengths:
            parts.append(f"优势：{insight.strengths}")
        if insight.triggers:
            parts.append(f"触发因素：{insight.triggers}")
    
    # 5. 用户记忆（重要的个性化信息）
    memories = db.query(UserMemory)\
        .filter(UserMemory.user_id == user_id)\
        .filter(UserMemory.importance >= 7)\
        .order_by(UserMemory.updated_at.desc())\
        .limit(5)\
        .all()
    
    if memories:
        memory_items = [f"- {m.content}" for m in memories]
        parts.append("重要记忆：\n" + "\n".join(memory_items))
    
    if not parts:
        return "（暂无用户画像信息）"
    
    return "\n".join(parts)


def add_user_memory(
    db: Session,
    user_id: int,
    role_id: int,
    memory_type: str,
    content: str,
    importance: int = 5
):
    """
    添加用户记忆
    memory_type: personality, preference, concern, goal, trigger, resource, event 等
    """
    memory = UserMemory(
        user_id=user_id,
        role_id=role_id,
        memory_type=memory_type,
        content=content,
        importance=importance
    )
    db.add(memory)
    db.commit()
    return memory


def get_user_memories(
    db: Session,
    user_id: int,
    role_id: int = None,
    memory_type: str = None,
    min_importance: int = 5,
    limit: int = 10
):
    """
    获取用户记忆
    role_id=None 时获取通用记忆
    """
    query = db.query(UserMemory).filter(UserMemory.user_id == user_id)
    
    if role_id is not None:
        # 获取该角色的记忆 + 通用记忆
        query = query.filter(
            (UserMemory.role_id == role_id) | (UserMemory.role_id == None)
        )
    
    if memory_type:
        query = query.filter(UserMemory.memory_type == memory_type)
    
    query = query.filter(UserMemory.importance >= min_importance)
    
    # 按重要性和更新时间排序
    query = query.order_by(
        UserMemory.importance.desc(),
        UserMemory.updated_at.desc()
    )
    
    return query.limit(limit).all()


def update_user_insight(db: Session, user_id: int, **kwargs):
    """
    更新用户深层洞察
    kwargs: core_traits, main_concerns, strengths, coping_patterns, triggers, summary
    """
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    
    if not insight:
        insight = UserInsight(user_id=user_id)
        db.add(insight)
    
    for key, value in kwargs.items():
        if hasattr(insight, key) and value is not None:
            setattr(insight, key, value)
    
    db.commit()
    db.refresh(insight)
    return insight


def extract_insights_from_conversation(
    db: Session,
    user_id: int,
    role_id: int,
    user_message: str,
    ai_response: str
):
    """
    从对话中提取洞察并更新用户记忆
    这里简化处理，实际可以调用 AI 来提取
    """
    # 简化版本：检测关键词
    keywords_personality = ["我是", "我总是", "我经常", "我的性格"]
    keywords_concern = ["担心", "焦虑", "困扰", "问题", "烦恼"]
    keywords_trigger = ["每当", "一旦", "就会", "触发"]
    keywords_goal = ["希望", "想要", "目标", "打算"]
    
    # 检测性格特质
    for kw in keywords_personality:
        if kw in user_message:
            # 提取相关句子作为记忆
            sentences = user_message.split("。")
            for sent in sentences:
                if kw in sent:
                    add_user_memory(
                        db, user_id, role_id,
                        memory_type="personality",
                        content=sent.strip(),
                        importance=6
                    )
    
    # 检测困扰
    for kw in keywords_concern:
        if kw in user_message:
            sentences = user_message.split("。")
            for sent in sentences:
                if kw in sent:
                    add_user_memory(
                        db, user_id, role_id,
                        memory_type="concern",
                        content=sent.strip(),
                        importance=7
                    )
    
    # 检测触发因素
    for kw in keywords_trigger:
        if kw in user_message:
            sentences = user_message.split("。")
            for sent in sentences:
                if kw in sent:
                    add_user_memory(
                        db, user_id, role_id,
                        memory_type="trigger",
                        content=sent.strip(),
                        importance=8
                    )
    
    # 检测目标
    for kw in keywords_goal:
        if kw in user_message:
            sentences = user_message.split("。")
            for sent in sentences:
                if kw in sent:
                    add_user_memory(
                        db, user_id, role_id,
                        memory_type="goal",
                        content=sent.strip(),
                        importance=7
                    )

