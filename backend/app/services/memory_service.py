"""
用户记忆和画像服务
让 AI 角色通过长期交互逐渐了解用户
"""
from sqlalchemy.orm import Session
from app.models.user_memory import UserMemory, UserInsight
from app.models.user_profile import UserProfile
from app.models.psych_test import PsychTest
from app.models.daily_checkin import DailyCheckin
from app.models.recovery_plan import RecoveryPlan
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
    
    # 3. 最近打卡情况（详细分析）
    recent_checkins = db.query(DailyCheckin)\
        .filter(DailyCheckin.user_id == user_id)\
        .order_by(DailyCheckin.date.desc())\
        .limit(7)\
        .all()
    
    if recent_checkins:
        # 心情分析
        moods = [c.mood for c in recent_checkins if c.mood]
        if moods:
            mood_counts = {}
            for mood in moods:
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            dominant_mood = max(mood_counts, key=mood_counts.get)
            parts.append(f"近期心情：{', '.join(moods[:3])}（主要：{dominant_mood}）")
        
        # 睡眠分析
        sleep_hours = [c.sleep_hours for c in recent_checkins if c.sleep_hours is not None]
        if sleep_hours:
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            if avg_sleep < 6:
                sleep_status = "睡眠不足"
            elif avg_sleep > 9:
                sleep_status = "睡眠过多"
            else:
                sleep_status = "睡眠正常"
            parts.append(f"睡眠状况：平均{avg_sleep:.1f}小时/天（{sleep_status}）")
        
        # 任务完成情况
        tasks = [c.completed_tasks for c in recent_checkins if c.completed_tasks]
        if tasks:
            task_keywords = []
            for task_str in tasks:
                if task_str:
                    task_keywords.extend(task_str.split(','))
            # 统计高频任务关键词
            task_counts = {}
            for task in task_keywords:
                task = task.strip()
                if task:
                    task_counts[task] = task_counts.get(task, 0) + 1
            if task_counts:
                top_tasks = sorted(task_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                task_summary = ', '.join([f"{task}({count}次)" for task, count in top_tasks])
                parts.append(f"常完成任务：{task_summary}")
    
    # 4. 生活计划/恢复计划分析
    recovery_plans = db.query(RecoveryPlan)\
        .filter(RecoveryPlan.user_id == user_id)\
        .order_by(RecoveryPlan.created_at.desc())\
        .limit(3)\
        .all()
    
    if recovery_plans:
        plan_summary = []
        for plan in recovery_plans:
            stage_info = f"（{plan.stage}）" if plan.stage else ""
            # 提取计划的关键信息（前100个字符）
            plan_preview = plan.plan_text[:100] + "..." if len(plan.plan_text) > 100 else plan.plan_text
            plan_summary.append(f"{plan_preview}{stage_info}")
        
        parts.append("生活计划：\n" + "\n".join(plan_summary))
    
    # 5. 深层洞察（如果有）
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    if insight:
        if insight.main_concerns:
            parts.append(f"主要困扰：{insight.main_concerns}")
        if insight.strengths:
            parts.append(f"优势：{insight.strengths}")
        if insight.triggers:
            parts.append(f"触发因素：{insight.triggers}")
    
    # 6. 用户记忆（重要的个性化信息）
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
    将心理测评结果整合到用户画像中 - 生成专业详细的测评信息
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        test_type: 测评类型
        score: 得分
        result: 测评结果字典（包含level, subscale_scores, suggestion等）
    """
    from app.core.psych_questionnaires import QUESTIONNAIRES
    
    # 获取量表配置
    config = QUESTIONNAIRES.get(test_type, {})
    test_title = config.get("abbr", test_type)
    
    level = result.get("level", "未知")
    color = result.get("color", "gray")
    suggestion = result.get("suggestion", "")
    
    # 根据测评类型和结果，生成专业的测评信息描述
    insight_updates = {}
    
    # ==================== 1. 情绪与心境类 ====================
    if test_type == "PHQ9":
        # PHQ-9 抑郁评估
        if score >= 10:  # 中度及以上
            professional_desc = f"""【抑郁症状评估 - PHQ-9】
等级: {level} (总分 {score}/27)
临床意义: """
            if score >= 20:
                professional_desc += "重度抑郁症状，强烈建议寻求专业心理/精神科医生评估。可能需要药物治疗结合心理治疗。"
            elif score >= 15:
                professional_desc += "中重度抑郁症状，建议尽快寻求专业帮助。心理咨询或认知行为疗法(CBT)可能有效。"
            elif score >= 10:
                professional_desc += "中度抑郁症状，建议考虑心理咨询。可以尝试自我调节（运动、社交、正念）结合专业支持。"
            
            professional_desc += f"\n主要表现: {_extract_phq9_symptoms(score)}"
            professional_desc += f"\n专业建议: {suggestion[:100]}..."
            
            insight_updates["main_concerns"] = professional_desc
    
    elif test_type == "GAD7":
        # GAD-7 焦虑评估
        if score >= 10:  # 中度及以上
            professional_desc = f"""【焦虑症状评估 - GAD-7】
等级: {level} (总分 {score}/21)
临床意义: """
            if score >= 15:
                professional_desc += "重度焦虑症状，建议专业评估。可能需要药物治疗和/或认知行为疗法。"
            elif score >= 10:
                professional_desc += "中度焦虑症状，建议寻求心理咨询。CBT、正念减压(MBSR)等方法有效。"
            
            professional_desc += f"\n主要表现: 过度担忧、紧张不安、难以放松、坐立不安"
            professional_desc += f"\n专业建议: {suggestion[:100]}..."
            
            # 追加而非替换
            existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
            current_concerns = existing_insight.main_concerns if existing_insight and existing_insight.main_concerns else ""
            if current_concerns:
                insight_updates["main_concerns"] = f"{current_concerns}\n\n{professional_desc}"
            else:
                insight_updates["main_concerns"] = professional_desc
    
    elif test_type == "PSS14":
        # PSS-14 压力知觉评估
        if score >= 28:  # 高压力
            professional_desc = f"""【压力知觉评估 - PSS-14】
等级: {level} (总分 {score}/56)
临床意义: 压力知觉水平较高，可能影响身心健康。长期高压力与焦虑、抑郁、心血管疾病等相关。
主要来源: 时间失控感、应对困难、情绪压力累积
专业建议: {suggestion[:150]}..."""
            
            existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
            current_concerns = existing_insight.main_concerns if existing_insight and existing_insight.main_concerns else ""
            if current_concerns:
                insight_updates["main_concerns"] = f"{current_concerns}\n\n{professional_desc}"
            else:
                insight_updates["main_concerns"] = professional_desc
    
    elif test_type == "PANAS":
        # PANAS 情绪评估
        subscale_scores = result.get("subscale_scores", {})
        pos_score = subscale_scores.get("积极情绪", 0)
        neg_score = subscale_scores.get("消极情绪", 0)
        
        professional_desc = f"""【情绪状态评估 - PANAS】
积极情绪: {pos_score}/50 ({_panas_level(pos_score, True)})
消极情绪: {neg_score}/50 ({_panas_level(neg_score, False)})
情绪平衡: """
        
        if pos_score >= 35 and neg_score <= 20:
            professional_desc += "良好，积极情绪充沛，消极情绪控制良好"
            # 更新优势
            insight_updates["strengths"] = _update_strength(db, user_id, "情绪调节良好，积极情绪丰富")
        elif pos_score < 25 or neg_score >= 30:
            professional_desc += "需关注，建议通过积极心理学干预提升积极情绪，通过正念/CBT降低消极情绪"
            insight_updates["coping_patterns"] = professional_desc
        else:
            professional_desc += "中等水平"
            insight_updates["coping_patterns"] = professional_desc
    
    # ==================== 2. 人际关系类 ====================
    elif test_type == "ECR36":
        # ECR-36 依恋风格评估
        subscale_scores = result.get("subscale_scores", {})
        subscale_levels = result.get("subscale_levels", {})
        anxiety_score = subscale_scores.get("关系焦虑", 0)
        avoidance_score = subscale_scores.get("关系回避", 0)
        anxiety_level = subscale_levels.get("关系焦虑", "")
        avoidance_level = subscale_levels.get("关系回避", "")
        
        professional_desc = f"""【依恋风格评估 - ECR-36】
关系焦虑: {anxiety_score}/126 ({anxiety_level})
  - 反映对被抛弃的恐惧、需要保证、担心伴侣不够在意自己
关系回避: {avoidance_score}/126 ({avoidance_level})
  - 反映对亲密的不适、难以依赖他人、情感表达困难

依恋类型判断: {_ecr_attachment_type(anxiety_level, avoidance_level)}
临床意义: """
        
        if "高" in anxiety_level or "高" in avoidance_level:
            professional_desc += "存在不安全依恋模式，可能影响亲密关系质量。"
            if "高" in anxiety_level:
                professional_desc += "建议关注自我价值感提升、焦虑管理。"
            if "高" in avoidance_level:
                professional_desc += "建议练习情感表达、建立信任。"
            professional_desc += "\n推荐: 情绪聚焦疗法(EFT)、依恋导向的伴侣治疗"
        else:
            professional_desc += "依恋模式相对安全，有助于建立稳定的亲密关系。"
        
        insight_updates["coping_patterns"] = professional_desc
    
    elif test_type == "IRI28":
        # IRI-28 共情能力评估
        subscale_scores = result.get("subscale_scores", {})
        subscale_levels = result.get("subscale_levels", {})
        
        professional_desc = f"""【共情能力评估 - IRI-28】
观点采择: {subscale_scores.get('观点采择', 0)}/28 ({subscale_levels.get('观点采择', '')})
  - 理解他人立场和视角的认知能力
幻想: {subscale_scores.get('幻想', 0)}/28 ({subscale_levels.get('幻想', '')})
  - 投入虚构世界的想象倾向
共情关注: {subscale_scores.get('共情关注', 0)}/28 ({subscale_levels.get('共情关注', '')})
  - 对他人困境的关心和同情
个人痛苦: {subscale_scores.get('个人痛苦', 0)}/28 ({subscale_levels.get('个人痛苦', '')})
  - 面对他人痛苦时的焦虑和不适"""
        
        # 提取优势
        strengths = []
        if "高" in subscale_levels.get("观点采择", ""):
            strengths.append("善于理解他人、换位思考能力强")
        if "高" in subscale_levels.get("共情关注", ""):
            strengths.append("富有同情心、关心他人")
        
        if strengths:
            insight_updates["strengths"] = _update_strength(db, user_id, ", ".join(strengths))
        
        # 如果个人痛苦过高，记录应对模式
        if "高" in subscale_levels.get("个人痛苦", ""):
            professional_desc += "\n\n需关注: 共情痛苦(empathic distress)较高，建议学习情绪边界设置，避免过度共情导致的二次创伤。"
            insight_updates["coping_patterns"] = professional_desc
        else:
            insight_updates["coping_patterns"] = professional_desc
    
    # ==================== 3. 自我认知类 ====================
    elif test_type == "RSES":
        # RSES 自尊评估
        professional_desc = f"""【自尊水平评估 - RSES】
总分: {score}/40
等级: {level}
临床意义: """
        
        if score < 30:
            professional_desc += "自尊水平较低，可能存在负面自我评价、自我价值感不足。与抑郁、焦虑风险相关。"
            professional_desc += "\n建议: 认知重构(CBT)、自我同情练习(Self-Compassion)、优势识别"
            insight_updates["core_traits"] = professional_desc
        elif score >= 30 and score < 35:
            professional_desc += "自尊水平中等，可通过肯定自己的成就和优点进一步提升。"
            insight_updates["core_traits"] = professional_desc
        else:
            professional_desc += "自尊水平良好，对自己有积极的评价，有助于心理韧性。"
            insight_updates["strengths"] = _update_strength(db, user_id, "自尊感良好，自我接纳度高")
    
    elif test_type == "SCS26":
        # SCS-26 自我同情评估
        subscale_scores = result.get("subscale_scores", {})
        subscale_levels = result.get("subscale_levels", {})
        
        professional_desc = f"""【自我同情评估 - SCS-26】
平均分: {score:.2f}/7
等级: {level}

六个维度:
• 自我友善: {subscale_scores.get('自我友善', 0):.2f} ({subscale_levels.get('自我友善', '')})
• 自我批判: {subscale_scores.get('自我批判', 0):.2f} ({subscale_levels.get('自我批判', '')}) [反向]
• 普遍人性: {subscale_scores.get('普遍人性', 0):.2f} ({subscale_levels.get('普遍人性', '')})
• 孤立: {subscale_scores.get('孤立', 0):.2f} ({subscale_levels.get('孤立', '')}) [反向]
• 正念: {subscale_scores.get('正念', 0):.2f} ({subscale_levels.get('正念', '')})
• 过度认同: {subscale_scores.get('过度认同', 0):.2f} ({subscale_levels.get('过度认同', '')}) [反向]

临床意义: """
        
        if score < 2.5:
            professional_desc += "自我同情水平较低，可能对自己过于苛刻。建议学习自我关怀技巧(Kristin Neff的自我同情练习)。"
        elif score >= 3.5:
            professional_desc += "自我同情水平良好，能以友善和理解的态度对待自己。"
            insight_updates["strengths"] = _update_strength(db, user_id, "自我同情水平高，善于自我关怀")
        else:
            professional_desc += "自我同情水平中等，可通过练习进一步提升。"
        
        insight_updates["core_traits"] = professional_desc
    
    # ==================== 4. 职场与学业类 ====================
    elif test_type == "MBI22":
        # MBI-22 职业倦怠评估
        subscale_scores = result.get("subscale_scores", {})
        subscale_levels = result.get("subscale_levels", {})
        
        professional_desc = f"""【职业倦怠评估 - MBI-22】
情绪耗竭: {subscale_scores.get('情绪耗竭', 0)}/54 ({subscale_levels.get('情绪耗竭', '')})
  - 精疲力竭、情感资源耗尽、无力应对工作
去人格化: {subscale_scores.get('去人格化', 0)}/30 ({subscale_levels.get('去人格化', '')})
  - 对工作对象冷漠、疏离、玩世不恭
个人成就感: {subscale_scores.get('个人成就感', 0)}/48 ({subscale_levels.get('个人成就感', '')})
  - 工作效能感和成就感的自我评价

综合评估: """
        
        if "高" in subscale_levels.get("情绪耗竭", "") or "高" in subscale_levels.get("去人格化", ""):
            professional_desc += "存在明显职业倦怠症状，建议：\n"
            professional_desc += "1. 工作-生活平衡调整\n"
            professional_desc += "2. 压力管理技巧(正念、放松训练)\n"
            professional_desc += "3. 社会支持系统建立\n"
            professional_desc += "4. 必要时寻求职业心理咨询"
            
            existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
            current_concerns = existing_insight.main_concerns if existing_insight and existing_insight.main_concerns else ""
            if current_concerns:
                insight_updates["main_concerns"] = f"{current_concerns}\n\n{professional_desc}"
            else:
                insight_updates["main_concerns"] = professional_desc
        else:
            professional_desc += "职业倦怠水平在可控范围内。"
            insight_updates["coping_patterns"] = professional_desc
    
    # ==================== 5. 创伤与应激类 ====================
    elif test_type == "PCL5_20":
        # PCL-5 PTSD评估
        subscale_scores = result.get("subscale_scores", {})
        subscale_levels = result.get("subscale_levels", {})
        
        professional_desc = f"""【创伤后应激障碍评估 - PCL-5】
总分: {score}/80
等级: {level}

DSM-5 四个症状簇:
B. 侵入症状: {subscale_scores.get('侵入症状', 0)}/20 ({subscale_levels.get('侵入症状', '')})
   - 闯入性记忆、噩梦、闪回
C. 回避症状: {subscale_scores.get('回避症状', 0)}/8 ({subscale_levels.get('回避症状', '')})
   - 回避创伤相关的想法、感受、提示
D. 负性改变: {subscale_scores.get('认知情绪负性改变', 0)}/28 ({subscale_levels.get('认知情绪负性改变', '')})
   - 负面信念、情绪麻木、兴趣丧失
E. 警觉改变: {subscale_scores.get('警觉性改变', 0)}/24 ({subscale_levels.get('警觉性改变', '')})
   - 过度警觉、易受惊吓、注意力问题

临床意义: """
        
        if score >= 31:  # 中度及以上
            professional_desc += "存在显著PTSD症状，强烈建议寻求创伤专科治疗。"
            professional_desc += "\n推荐疗法: EMDR(眼动脱敏再处理)、创伤聚焦CBT、叙事暴露疗法"
            professional_desc += "\n重要: 创伤治疗需专业指导，切勿自行处理创伤记忆"
            insight_updates["triggers"] = professional_desc
        elif score >= 21:
            professional_desc += "存在轻度PTSD症状，建议心理咨询评估。"
            insight_updates["triggers"] = professional_desc
        else:
            professional_desc += "PTSD症状轻微或不显著。"
    
    # 应用更新
    if insight_updates:
        update_user_insight(db, user_id, **insight_updates)
        print(f"[INFO] 已更新用户 {user_id} 的专业测评画像，更新字段: {list(insight_updates.keys())}")


# ==================== 辅助函数 ====================

def _extract_phq9_symptoms(score: int) -> str:
    """根据PHQ-9分数推断可能的主要症状"""
    if score >= 20:
        return "兴趣丧失、情绪低落、疲劳、睡眠障碍、食欲改变、负罪感、注意力下降、动作迟缓/激越、自杀意念"
    elif score >= 15:
        return "明显的兴趣丧失、情绪低落、疲劳、睡眠或食欲问题、注意力下降"
    elif score >= 10:
        return "兴趣下降、心情郁闷、疲倦、部分睡眠或食欲改变"
    else:
        return "轻微情绪波动"


def _panas_level(score: int, is_positive: bool) -> str:
    """PANAS 情绪水平判断"""
    if is_positive:
        if score >= 35:
            return "高水平"
        elif score >= 25:
            return "中等水平"
        else:
            return "低水平"
    else:  # negative
        if score >= 30:
            return "高水平(需关注)"
        elif score >= 20:
            return "中等水平"
        else:
            return "低水平(良好)"


def _ecr_attachment_type(anxiety: str, avoidance: str) -> str:
    """ECR-36 依恋类型判断"""
    if "低" in anxiety and "低" in avoidance:
        return "安全型依恋 (Secure) - 能建立稳定亲密关系，信任他人，情感表达流畅"
    elif "高" in anxiety and "低" in avoidance:
        return "焦虑型依恋 (Anxious/Preoccupied) - 渴望亲密但担心被抛弃，需要频繁保证"
    elif "低" in anxiety and "高" in avoidance:
        return "回避型依恋 (Avoidant/Dismissing) - 不适亲密，强调独立，情感表达困难"
    elif "高" in anxiety and "高" in avoidance:
        return "恐惧型依恋 (Fearful-Avoidant) - 渴望但恐惧亲密，矛盾心理明显"
    else:
        return "中等水平，部分依恋模式特征"


def _update_strength(db: Session, user_id: int, new_strength: str) -> str:
    """追加优势信息，避免覆盖"""
    existing_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    current_strengths = existing_insight.strengths if existing_insight and existing_insight.strengths else ""
    
    if current_strengths and new_strength not in current_strengths:
        return f"{current_strengths}; {new_strength}"
    elif not current_strengths:
        return new_strength
    else:
        return current_strengths


def update_profile_with_checkin(db: Session, user_id: int, checkin_data: dict):
    """
    根据每日打卡数据更新用户画像
    """
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    if not insight:
        insight = UserInsight(user_id=user_id)
        db.add(insight)
    
    updates = {}
    
    # 分析心情模式
    if checkin_data.get('mood'):
        mood = checkin_data['mood']
        mood_insights = {
            '开心': '用户表现出积极情绪，具有乐观的生活态度',
            '平静': '用户情绪稳定，具有良好的情绪调节能力',
            '焦虑': '用户可能面临压力，需要关注焦虑管理',
            '沮丧': '用户可能遇到困难，需要情感支持',
            '愤怒': '用户可能面临挫折，需要情绪疏导',
            '疲惫': '用户可能过度劳累，需要休息调整'
        }
        
        if mood in mood_insights:
            mood_insight = mood_insights[mood]
            if 'coping_patterns' not in updates:
                updates['coping_patterns'] = insight.coping_patterns or ""
            if mood_insight not in updates['coping_patterns']:
                updates['coping_patterns'] = f"{updates['coping_patterns']}\n- {mood_insight}".strip()
    
    # 分析睡眠模式
    if checkin_data.get('sleep_hours') is not None:
        sleep_hours = checkin_data['sleep_hours']
        if sleep_hours < 6:
            sleep_insight = "睡眠不足，可能影响情绪和认知功能"
        elif sleep_hours > 9:
            sleep_insight = "睡眠过多，可能存在抑郁或疲劳问题"
        else:
            sleep_insight = "睡眠规律，有利于身心健康"
        
        if 'coping_patterns' not in updates:
            updates['coping_patterns'] = insight.coping_patterns or ""
        if sleep_insight not in updates['coping_patterns']:
            updates['coping_patterns'] = f"{updates['coping_patterns']}\n- {sleep_insight}".strip()
    
    # 分析任务完成情况
    if checkin_data.get('completed_tasks'):
        tasks = checkin_data['completed_tasks']
        if isinstance(tasks, str):
            task_list = [t.strip() for t in tasks.split(',') if t.strip()]
        else:
            task_list = tasks
        
        if task_list:
            # 分析任务类型
            work_tasks = [t for t in task_list if any(keyword in t.lower() for keyword in ['工作', '项目', '会议', '报告', '任务'])]
            health_tasks = [t for t in task_list if any(keyword in t.lower() for keyword in ['运动', '锻炼', '健身', '跑步', '瑜伽'])]
            social_tasks = [t for t in task_list if any(keyword in t.lower() for keyword in ['朋友', '家人', '聚会', '聊天'])]
            
            if work_tasks:
                work_insight = f"用户注重工作效率，完成工作相关任务：{', '.join(work_tasks[:2])}"
                if 'strengths' not in updates:
                    updates['strengths'] = insight.strengths or ""
                if work_insight not in updates['strengths']:
                    updates['strengths'] = f"{updates['strengths']}\n- {work_insight}".strip()
            
            if health_tasks:
                health_insight = f"用户重视健康管理，坚持健康活动：{', '.join(health_tasks[:2])}"
                if 'strengths' not in updates:
                    updates['strengths'] = insight.strengths or ""
                if health_insight not in updates['strengths']:
                    updates['strengths'] = f"{updates['strengths']}\n- {health_insight}".strip()
            
            if social_tasks:
                social_insight = f"用户重视人际关系，积极参与社交活动：{', '.join(social_tasks[:2])}"
                if 'strengths' not in updates:
                    updates['strengths'] = insight.strengths or ""
                if social_insight not in updates['strengths']:
                    updates['strengths'] = f"{updates['strengths']}\n- {social_insight}".strip()
    
    # 更新数据库
    for field, value in updates.items():
        setattr(insight, field, value)
    
    db.commit()
    print(f"[INFO] 已更新用户 {user_id} 的打卡画像: {updates}")


def update_profile_with_recovery_plan(db: Session, user_id: int, plan_data: dict):
    """
    根据生活计划/恢复计划更新用户画像
    """
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    if not insight:
        insight = UserInsight(user_id=user_id)
        db.add(insight)
    
    updates = {}
    plan_text = plan_data.get('plan_text', '')
    stage = plan_data.get('stage', '')
    
    # 分析计划内容，提取关键信息
    if plan_text:
        # 分析计划中的关键词
        plan_lower = plan_text.lower()
        
        # 识别主要关注领域
        concerns = []
        if any(keyword in plan_lower for keyword in ['焦虑', '紧张', '担心', '恐惧']):
            concerns.append('焦虑管理')
        if any(keyword in plan_lower for keyword in ['抑郁', '低落', '悲伤', '绝望']):
            concerns.append('情绪调节')
        if any(keyword in plan_lower for keyword in ['压力', '负担', '累', '疲惫']):
            concerns.append('压力管理')
        if any(keyword in plan_lower for keyword in ['睡眠', '失眠', '作息']):
            concerns.append('睡眠改善')
        if any(keyword in plan_lower for keyword in ['社交', '朋友', '人际关系']):
            concerns.append('社交技能')
        
        if concerns:
            concern_text = f"用户关注的主要领域：{', '.join(concerns)}"
            if 'main_concerns' not in updates:
                updates['main_concerns'] = insight.main_concerns or ""
            if concern_text not in updates['main_concerns']:
                updates['main_concerns'] = f"{updates['main_concerns']}\n- {concern_text}".strip()
        
        # 识别应对策略
        strategies = []
        if any(keyword in plan_lower for keyword in ['冥想', '正念', '呼吸', '放松']):
            strategies.append('正念练习')
        if any(keyword in plan_lower for keyword in ['运动', '锻炼', '健身', '跑步']):
            strategies.append('运动疗法')
        if any(keyword in plan_lower for keyword in ['日记', '记录', '反思', '总结']):
            strategies.append('自我反思')
        if any(keyword in plan_lower for keyword in ['目标', '计划', '步骤', '阶段']):
            strategies.append('目标设定')
        if any(keyword in plan_lower for keyword in ['支持', '帮助', '咨询', '治疗']):
            strategies.append('寻求支持')
        
        if strategies:
            strategy_text = f"用户采用的应对策略：{', '.join(strategies)}"
            if 'coping_patterns' not in updates:
                updates['coping_patterns'] = insight.coping_patterns or ""
            if strategy_text not in updates['coping_patterns']:
                updates['coping_patterns'] = f"{updates['coping_patterns']}\n- {strategy_text}".strip()
        
        # 识别个人优势
        strengths = []
        if any(keyword in plan_lower for keyword in ['坚持', '持续', '努力', '积极']):
            strengths.append('坚持性')
        if any(keyword in plan_lower for keyword in ['学习', '成长', '进步', '改善']):
            strengths.append('学习能力')
        if any(keyword in plan_lower for keyword in ['自我', '独立', '自主', '负责']):
            strengths.append('自我管理')
        if any(keyword in plan_lower for keyword in ['乐观', '希望', '信心', '积极']):
            strengths.append('乐观态度')
        
        if strengths:
            strength_text = f"用户展现的个人优势：{', '.join(strengths)}"
            if 'strengths' not in updates:
                updates['strengths'] = insight.strengths or ""
            if strength_text not in updates['strengths']:
                updates['strengths'] = f"{updates['strengths']}\n- {strength_text}".strip()
    
    # 更新阶段信息
    if stage:
        stage_insight = f"当前恢复阶段：{stage}"
        if 'core_traits' not in updates:
            updates['core_traits'] = insight.core_traits or ""
        if stage_insight not in updates['core_traits']:
            updates['core_traits'] = f"{updates['core_traits']}\n- {stage_insight}".strip()
    
    # 更新数据库
    for field, value in updates.items():
        setattr(insight, field, value)
    
    db.commit()
    print(f"[INFO] 已更新用户 {user_id} 的计划画像: {updates}")

