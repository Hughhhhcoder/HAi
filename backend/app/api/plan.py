from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_profile import UserProfile
from app.models.recovery_plan import RecoveryPlan
from app.models.psych_test import PsychTest
from app.services.memory_service import update_profile_with_recovery_plan, update_profile_with_checkin
from app.services.plan_service import generate_smart_recovery_plan
import json
from datetime import datetime

router = APIRouter(prefix="/api/plan", tags=["plan"])

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 录入/更新作息信息
@router.post("/profile")
def update_profile(
    user_id: int = Form(...),
    sleep_time: str | None = Form(None),
    wake_time: str | None = Form(None),
    preferences: str | None = Form(None),
    db: Session = Depends(get_db)
):
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
    
    # 实时更新用户画像
    try:
        # 构建作息数据用于画像更新
        schedule_data = {
            'sleep_time': sleep_time,
            'wake_time': wake_time,
            'preferences': preferences or ''
        }
        update_profile_with_checkin(db, user_id, schedule_data)
        print(f"[INFO] 已更新用户 {user_id} 的作息画像")
    except Exception as e:
        print(f"[WARN] 更新作息画像失败: {e}")
    
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

# 生成智能生活恢复计划
@router.post("/generate")
def generate_plan(user_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        # 使用新的智能计划生成服务
        plan_data = generate_smart_recovery_plan(db, user_id)
        
        # 创建计划记录
        plan = RecoveryPlan(
            user_id=user_id, 
            plan_text=plan_data["plan_text"], 
            stage=plan_data["stage"]
        )
        db.add(plan)
        
        # 更新用户画像
        update_profile_with_recovery_plan(db, user_id, {
            'plan_text': plan_data["plan_text"],
            'stage': plan_data["stage"]
        })
        
        db.commit()
        db.refresh(plan)
        
        return {
            "plan_id": plan.id, 
            "plan_text": plan.plan_text, 
            "stage": plan.stage,
            "focus_areas": plan_data.get("focus_areas", []),
            "priority_level": plan_data.get("priority_level", "中等")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成计划失败：{str(e)}")

# 查询历史计划
@router.get("/history")
def plan_history(user_id: int, db: Session = Depends(get_db)):
    plans = db.query(RecoveryPlan).filter(RecoveryPlan.user_id == user_id).order_by(RecoveryPlan.created_at.desc()).all()
    return [{
        "id": p.id,
        "plan_text": p.plan_text,
        "stage": p.stage,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None
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