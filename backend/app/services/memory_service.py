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
    
    # 2. 最近的心理测评结果（详细版，包含等级和维度）
    recent_tests = db.query(PsychTest)\
        .filter(PsychTest.user_id == user_id)\
        .order_by(PsychTest.date.desc())\
        .limit(3)\
        .all()
    
    if recent_tests:
        test_summary = []
        for test in recent_tests:
            # 解析 result_json 获取详细信息
            try:
                result = json.loads(test.result_json) if test.result_json else {}
                level = result.get("level", "未知")
                test_summary.append(f"{test.test_type}={level}({test.score}分)")
                
                # 如果有分量表，添加关键维度
                if "subscale_levels" in result:
                    subscales = result.get("subscale_levels", {})
                    for sub_name, sub_level in list(subscales.items())[:2]:  # 最多显示2个维度
                        test_summary.append(f"  └ {sub_name}={sub_level}")
            except:
                test_summary.append(f"{test.test_type}={test.score}分")
        
        parts.append(f"近期心理测评：\n" + "\n".join(test_summary))
    
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


def update_profile_with_psych_test(
    db: Session,
    user_id: int,
    test_type: str,
    score: int,
    result: dict
):
    """
    将心理测评结果整合到用户画像中
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        test_type: 测评类型
        score: 得分
        result: 测评结果字典（包含level, subscale_scores等）
    """
    level = result.get("level", "未知")
    
    # 根据测评类型和结果，提取关键洞察
    insight_updates = {}
    
    # 1. 情绪与心境类 - 更新主要困扰
    if test_type in ["PHQ9", "GAD7", "PSS14"]:
        concern_map = {
            "PHQ9": "抑郁",
            "GAD7": "焦虑",
            "PSS14": "压力"
        }
        concern_type = concern_map.get(test_type, "情绪")
        
        if level in ["中度", "中重度", "重度", "高压力"]:
            # 更新主要困扰
            existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
            current_concerns = existing_insight.main_concerns if existing_insight and existing_insight.main_concerns else ""
            
            if concern_type not in current_concerns:
                new_concerns = f"{current_concerns}, {concern_type}({level})" if current_concerns else f"{concern_type}({level})"
                insight_updates["main_concerns"] = new_concerns.strip(", ")
    
    # 2. 人际关系类 - 更新人际模式
    if test_type == "ECR36":
        subscale_levels = result.get("subscale_levels", {})
        anxiety_level = subscale_levels.get("关系焦虑", "")
        avoidance_level = subscale_levels.get("关系回避", "")
        
        if anxiety_level or avoidance_level:
            coping_pattern = f"依恋风格: {anxiety_level}焦虑, {avoidance_level}回避"
            insight_updates["coping_patterns"] = coping_pattern
    
    # 3. 自我认知类 - 更新核心特质
    if test_type == "RSES":
        if level in ["低自尊", "中等自尊"]:
            insight_updates["core_traits"] = f"自尊水平: {level}"
    
    if test_type == "SCS26":
        if level in ["低自我同情", "中等自我同情"]:
            insight_updates["core_traits"] = f"自我同情: {level}"
    
    # 4. 职场倦怠 - 更新困扰
    if test_type == "MBI22":
        subscale_levels = result.get("subscale_levels", {})
        exhaustion = subscale_levels.get("情绪耗竭", "")
        
        if "高" in exhaustion or "中等" in exhaustion:
            existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
            current_concerns = existing_insight.main_concerns if existing_insight and existing_insight.main_concerns else ""
            
            if "职业倦怠" not in current_concerns:
                new_concerns = f"{current_concerns}, 职业倦怠({exhaustion}耗竭)" if current_concerns else f"职业倦怠({exhaustion}耗竭)"
                insight_updates["main_concerns"] = new_concerns.strip(", ")
    
    # 5. 创伤应激 - 更新触发因素
    if test_type == "PCL5_20":
        if level in ["中度PTSD症状", "重度PTSD症状"]:
            insight_updates["triggers"] = f"存在创伤后应激症状({level})"
    
    # 提取积极方面 - 更新优势
    strengths = []
    if test_type == "PANAS":
        subscale_scores = result.get("subscale_scores", {})
        positive_score = subscale_scores.get("积极情绪", 0)
        if positive_score >= 35:
            strengths.append("积极情绪丰富")
    
    if test_type == "RSES" and level == "高自尊":
        strengths.append("自尊感良好")
    
    if test_type == "IRI28":
        subscale_levels = result.get("subscale_levels", {})
        if "高" in subscale_levels.get("共情关注", ""):
            strengths.append("共情能力强")
        if "高" in subscale_levels.get("观点采择", ""):
            strengths.append("善于理解他人")
    
    if strengths:
        existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
        current_strengths = existing_insight.strengths if existing_insight and existing_insight.strengths else ""
        new_strengths_text = ", ".join(strengths)
        
        if current_strengths:
            insight_updates["strengths"] = f"{current_strengths}, {new_strengths_text}"
        else:
            insight_updates["strengths"] = new_strengths_text
    
    # 应用更新
    if insight_updates:
        update_user_insight(db, user_id, **insight_updates)
        print(f"[INFO] 已更新用户 {user_id} 的画像: {insight_updates}")

