from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_profile import UserProfile
from app.models.recovery_plan import RecoveryPlan
from app.models.psych_test import PsychTest
import json
from datetime import datetime

router = APIRouter(prefix="/plan", tags=["plan"])

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 录入/更新作息信息
@router.post("/profile")
def update_profile(user_id: int, sleep_time: str = None, wake_time: str = None, preferences: str = None, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
    if sleep_time:
        profile.sleep_time = sleep_time
    if wake_time:
        profile.wake_time = wake_time
    if preferences:
        profile.preferences = preferences
    db.commit()
    return {"msg": "作息信息已更新"}

# 获取作息信息
@router.get("/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="未找到作息信息")
    return {
        "user_id": profile.user_id,
        "sleep_time": profile.sleep_time,
        "wake_time": profile.wake_time,
        "preferences": profile.preferences
    }

# 生成生活恢复计划（mock智能）
@router.post("/generate")
def generate_plan(user_id: int, db: Session = Depends(get_db)):
    # 获取作息
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="请先录入作息信息")
    # 获取最近一次测评
    test = db.query(PsychTest).filter(PsychTest.user_id == user_id).order_by(PsychTest.date.desc()).first()
    # mock知识库检索
    knowledge = "保持规律作息、适度运动、均衡饮食、关注心理健康。"
    # 生成计划文本
    plan_text = build_plan_text(profile, test, knowledge)
    plan = RecoveryPlan(user_id=user_id, plan_text=plan_text, stage="第一阶段")
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {"plan_id": plan.id, "plan_text": plan.plan_text, "stage": plan.stage}

# 查询历史计划
@router.get("/history")
def plan_history(user_id: int, db: Session = Depends(get_db)):
    plans = db.query(RecoveryPlan).filter(RecoveryPlan.user_id == user_id).order_by(RecoveryPlan.created_at.desc()).all()
    return [{
        "id": p.id,
        "plan_text": p.plan_text,
        "stage": p.stage,
        "created_at": p.created_at
    } for p in plans]

# mock计划生成逻辑
def build_plan_text(profile, test, knowledge):
    base = f"【生活恢复计划】\n作息建议：建议每天{profile.wake_time or '7:00'}起床，{profile.sleep_time or '23:00'}睡觉。"
    if profile.preferences:
        base += f"\n个人偏好：{profile.preferences}"
    if test:
        base += f"\n心理测评（{test.test_type}）：分数{test.score}。"
        if test.score >= 10:
            base += "\n建议重点关注心理健康，必要时寻求专业帮助。"
        else:
            base += "\n心理状态良好，继续保持。"
    base += f"\n知识库建议：{knowledge}"
    base += "\n本阶段目标：规律作息、适度运动、保持积极心态。"
    return base 