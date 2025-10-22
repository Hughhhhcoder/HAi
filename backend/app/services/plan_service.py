"""
智能生活计划生成服务
主要基于用户作息和偏好，次要参考用户画像，生成个性化恢复计划
"""

from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.models.psych_test import PsychTest
from app.models.daily_checkin import DailyCheckin
from app.models.user_memory import UserInsight
from app.services.memory_service import get_user_profile_summary
import json
from datetime import datetime, timedelta


def generate_smart_recovery_plan(db: Session, user_id: int) -> dict:
    """
    生成智能生活恢复计划
    主要基于用户作息和偏好，次要参考用户画像
    """
    # 1. 获取用户基础信息（主要依据）
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise ValueError("请先录入作息信息")
    
    # 2. 获取用户画像（次要参考）
    user_insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    
    # 3. 获取最近测评结果（辅助参考）
    recent_test = db.query(PsychTest)\
        .filter(PsychTest.user_id == user_id)\
        .order_by(PsychTest.date.desc())\
        .first()
    
    # 4. 获取最近打卡情况（辅助参考）
    recent_checkins = db.query(DailyCheckin)\
        .filter(DailyCheckin.user_id == user_id)\
        .order_by(DailyCheckin.date.desc())\
        .limit(7)\
        .all()
    
    # 5. 生成个性化计划
    plan_data = _build_smart_plan(profile, user_insight, recent_test, recent_checkins)
    
    return plan_data


def _build_smart_plan(profile, user_insight, recent_test, recent_checkins) -> dict:
    """
    构建智能计划内容
    """
    plan_parts = []
    
    # === 主要部分：基于作息和偏好 ===
    plan_parts.append("【个性化生活恢复计划】")
    plan_parts.append("")
    
    # 1. 作息建议（主要依据）
    if profile.sleep_time and profile.wake_time:
        wake_time = profile.wake_time
        sleep_time = profile.sleep_time
        
        # 分析作息合理性
        wake_hour = int(wake_time.split(':')[0])
        sleep_hour = int(sleep_time.split(':')[0])
        
        if sleep_hour < 12:  # 晚上睡觉
            sleep_hour += 24
        
        sleep_duration = sleep_hour - wake_hour
        
        if sleep_duration < 7:
            sleep_advice = f"建议增加睡眠时间，当前{profile.wake_time}起床，{profile.sleep_time}睡觉，睡眠时长约{sleep_duration}小时，建议延长至7-9小时。"
        elif sleep_duration > 10:
            sleep_advice = f"当前睡眠时间较长，{profile.wake_time}起床，{profile.sleep_time}睡觉，建议适当调整作息，保持7-9小时睡眠。"
        else:
            sleep_advice = f"作息时间合理，建议保持{profile.wake_time}起床，{profile.sleep_time}睡觉的良好习惯。"
        
        plan_parts.append("🕐 作息建议：")
        plan_parts.append(f"• {sleep_advice}")
        plan_parts.append(f"• 建议固定作息时间，避免熬夜和睡懒觉")
        plan_parts.append("")
    else:
        plan_parts.append("🕐 作息建议：")
        plan_parts.append("• 建议建立规律的作息时间，早睡早起")
        plan_parts.append("• 推荐作息：7:00起床，23:00睡觉")
        plan_parts.append("")
    
    # 2. 个人偏好定制（主要依据）
    if profile.preferences:
        preferences = profile.preferences.strip()
        plan_parts.append("💝 个人偏好定制：")
        
        # 分析偏好内容，生成个性化建议
        if any(keyword in preferences for keyword in ['运动', '健身', '锻炼', '跑步', '瑜伽']):
            plan_parts.append("• 根据您的运动偏好，建议制定规律的运动计划")
            plan_parts.append("• 推荐：每周3-4次运动，每次30-45分钟")
        else:
            plan_parts.append("• 建议增加适量运动，有助于身心健康")
        
        if any(keyword in preferences for keyword in ['学习', '读书', '阅读', '知识']):
            plan_parts.append("• 结合您的学习兴趣，建议安排固定的学习时间")
            plan_parts.append("• 推荐：每天30-60分钟的学习时间")
        
        if any(keyword in preferences for keyword in ['社交', '朋友', '聚会', '聊天']):
            plan_parts.append("• 重视社交活动，建议保持与朋友的联系")
            plan_parts.append("• 推荐：每周至少1-2次社交活动")
        
        if any(keyword in preferences for keyword in ['放松', '休息', '娱乐', '游戏', '音乐']):
            plan_parts.append("• 合理安排娱乐时间，劳逸结合")
            plan_parts.append("• 推荐：每天1-2小时的放松时间")
        
        plan_parts.append(f"• 您的偏好：{preferences}")
        plan_parts.append("")
    else:
        plan_parts.append("💝 个人偏好定制：")
        plan_parts.append("• 建议探索个人兴趣爱好，丰富生活内容")
        plan_parts.append("• 可以尝试运动、学习、社交、娱乐等活动")
        plan_parts.append("")
    
    # === 次要部分：基于用户画像 ===
    if user_insight:
        plan_parts.append("🎯 个性化建议（基于您的画像）：")
        
        # 基于主要困扰
        if user_insight.main_concerns:
            concerns = user_insight.main_concerns
            if '焦虑' in concerns or '压力' in concerns:
                plan_parts.append("• 针对您的焦虑/压力问题，建议：")
                plan_parts.append("  - 每天进行10-15分钟的正念冥想")
                plan_parts.append("  - 学习深呼吸和放松技巧")
                plan_parts.append("  - 避免过度刺激的活动")
            
            if '抑郁' in concerns or '情绪' in concerns:
                plan_parts.append("• 针对您的情绪问题，建议：")
                plan_parts.append("  - 保持规律的作息和饮食")
                plan_parts.append("  - 多进行户外活动，接触阳光")
                plan_parts.append("  - 与信任的人分享感受")
            
            if '睡眠' in concerns:
                plan_parts.append("• 针对您的睡眠问题，建议：")
                plan_parts.append("  - 建立固定的睡前仪式")
                plan_parts.append("  - 避免睡前使用电子设备")
                plan_parts.append("  - 保持卧室环境舒适安静")
        
        # 基于优势
        if user_insight.strengths:
            strengths = user_insight.strengths
            if '坚持' in strengths or '努力' in strengths:
                plan_parts.append("• 发挥您的坚持优势，建议制定长期目标")
            if '学习' in strengths or '成长' in strengths:
                plan_parts.append("• 利用您的学习能力，建议持续自我提升")
            if '社交' in strengths or '人际关系' in strengths:
                plan_parts.append("• 发挥您的社交优势，建议多参与群体活动")
        
        # 基于应对模式
        if user_insight.coping_patterns:
            patterns = user_insight.coping_patterns
            if '正念' in patterns or '冥想' in patterns:
                plan_parts.append("• 继续您的正念练习，建议每天固定时间进行")
            if '运动' in patterns:
                plan_parts.append("• 保持您的运动习惯，建议制定运动计划")
            if '寻求支持' in patterns:
                plan_parts.append("• 继续寻求专业支持，建议定期咨询")
        
        plan_parts.append("")
    
    # === 辅助部分：基于测评和打卡数据 ===
    if recent_test:
        plan_parts.append("📊 心理状态参考：")
        try:
            result = json.loads(recent_test.result_json) if recent_test.result_json else {}
            level = result.get("level", "未知")
            plan_parts.append(f"• 最近测评（{recent_test.test_type}）：{level}（{recent_test.score}分）")
            
            if recent_test.score >= 10:
                plan_parts.append("• 建议重点关注心理健康，必要时寻求专业帮助")
            else:
                plan_parts.append("• 心理状态良好，继续保持当前状态")
        except:
            plan_parts.append(f"• 最近测评：{recent_test.test_type}（{recent_test.score}分）")
        plan_parts.append("")
    
    if recent_checkins:
        plan_parts.append("📈 近期状态分析：")
        
        # 心情分析
        moods = [c.mood for c in recent_checkins if c.mood]
        if moods:
            mood_counts = {}
            for mood in moods:
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            dominant_mood = max(mood_counts, key=mood_counts.get)
            plan_parts.append(f"• 近期心情：主要{dominant_mood}，建议关注情绪变化")
        
        # 睡眠分析
        sleep_hours = [c.sleep_hours for c in recent_checkins if c.sleep_hours is not None]
        if sleep_hours:
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            if avg_sleep < 6:
                plan_parts.append(f"• 睡眠状况：平均{avg_sleep:.1f}小时/天，建议增加睡眠时间")
            elif avg_sleep > 9:
                plan_parts.append(f"• 睡眠状况：平均{avg_sleep:.1f}小时/天，建议适当调整")
            else:
                plan_parts.append(f"• 睡眠状况：平均{avg_sleep:.1f}小时/天，保持良好")
        
        plan_parts.append("")
    
    # === 通用建议 ===
    plan_parts.append("🌟 通用健康建议：")
    plan_parts.append("• 保持规律作息，早睡早起")
    plan_parts.append("• 均衡饮食，多喝水，少食多餐")
    plan_parts.append("• 适量运动，每周至少150分钟中等强度运动")
    plan_parts.append("• 保持社交联系，与家人朋友多沟通")
    plan_parts.append("• 学会放松，培养兴趣爱好")
    plan_parts.append("• 定期自我反思，记录成长变化")
    plan_parts.append("")
    
    # === 阶段目标 ===
    plan_parts.append("🎯 本阶段目标：")
    plan_parts.append("• 建立稳定的作息规律")
    plan_parts.append("• 培养健康的生活习惯")
    plan_parts.append("• 提升心理韧性")
    plan_parts.append("• 增强自我管理能力")
    plan_parts.append("")
    
    plan_parts.append("💡 温馨提示：")
    plan_parts.append("• 计划需要根据实际情况灵活调整")
    plan_parts.append("• 建议每周回顾一次，评估进展")
    plan_parts.append("• 如有困难，及时寻求专业帮助")
    
    # 生成计划文本
    plan_text = "\n".join(plan_parts)
    
    # 确定阶段
    stage = _determine_stage(profile, user_insight, recent_test)
    
    return {
        "plan_text": plan_text,
        "stage": stage,
        "focus_areas": _extract_focus_areas(profile, user_insight),
        "priority_level": _determine_priority_level(user_insight, recent_test)
    }


def _determine_stage(profile, user_insight, recent_test) -> str:
    """确定恢复阶段"""
    if not user_insight:
        return "第一阶段：基础建立"
    
    # 基于用户画像确定阶段
    if user_insight.main_concerns:
        if any(keyword in user_insight.main_concerns for keyword in ['重度', '严重', '危机']):
            return "第一阶段：危机干预"
        elif any(keyword in user_insight.main_concerns for keyword in ['中度', '明显']):
            return "第二阶段：稳定改善"
        else:
            return "第三阶段：持续优化"
    
    return "第一阶段：基础建立"


def _extract_focus_areas(profile, user_insight) -> list:
    """提取重点关注的领域"""
    focus_areas = []
    
    # 基于作息
    if profile.sleep_time and profile.wake_time:
        focus_areas.append("作息规律")
    
    # 基于偏好
    if profile.preferences:
        if any(keyword in profile.preferences for keyword in ['运动', '健身']):
            focus_areas.append("运动健康")
        if any(keyword in profile.preferences for keyword in ['学习', '读书']):
            focus_areas.append("学习成长")
        if any(keyword in profile.preferences for keyword in ['社交', '朋友']):
            focus_areas.append("社交关系")
    
    # 基于用户画像
    if user_insight and user_insight.main_concerns:
        if '焦虑' in user_insight.main_concerns:
            focus_areas.append("焦虑管理")
        if '抑郁' in user_insight.main_concerns:
            focus_areas.append("情绪调节")
        if '睡眠' in user_insight.main_concerns:
            focus_areas.append("睡眠改善")
    
    return focus_areas if focus_areas else ["基础健康"]


def _determine_priority_level(user_insight, recent_test) -> str:
    """确定优先级"""
    if not user_insight and not recent_test:
        return "中等"
    
    # 基于测评结果
    if recent_test and recent_test.score >= 15:
        return "高"
    elif recent_test and recent_test.score >= 10:
        return "中高"
    
    # 基于用户画像
    if user_insight and user_insight.main_concerns:
        if any(keyword in user_insight.main_concerns for keyword in ['重度', '严重']):
            return "高"
        elif any(keyword in user_insight.main_concerns for keyword in ['中度', '明显']):
            return "中高"
    
    return "中等"
