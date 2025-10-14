from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.daily_checkin import DailyCheckin
from app.models.reward import Reward
from datetime import date

router = APIRouter(prefix="/checkin", tags=["checkin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 每日打卡
@router.post("/daily")
def daily_checkin(
    user_id: int = Form(...),
    mood: str | None = Form(None),
    sleep_hours: float | None = Form(None),
    completed_tasks: str | None = Form(None),
    db: Session = Depends(get_db)
):
    today = date.today()
    # 检查是否已打卡
    record = db.query(DailyCheckin).filter(DailyCheckin.user_id == user_id, DailyCheckin.date == today).first()
    if record:
        raise HTTPException(status_code=400, detail="今日已打卡")
    # 新增打卡
    record = DailyCheckin(user_id=user_id, date=today, mood=mood, sleep_hours=sleep_hours, completed_tasks=completed_tasks)
    db.add(record)
    # 积分奖励
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        reward = Reward(user_id=user_id, points=0, reward_history="")
        db.add(reward)
    reward.points += 5  # 每日打卡+5分
    reward.reward_history = (reward.reward_history or "") + f"{today}:每日打卡+5分,"
    db.commit()
    return {"msg": "打卡成功，积分+5", "points": reward.points}

# 打卡历史
@router.get("/history")
def checkin_history(user_id: int, db: Session = Depends(get_db)):
    records = db.query(DailyCheckin).filter(DailyCheckin.user_id == user_id).order_by(DailyCheckin.date.desc()).all()
    return [{
        "date": r.date,
        "mood": r.mood,
        "sleep_hours": r.sleep_hours,
        "completed_tasks": r.completed_tasks
    } for r in records] 