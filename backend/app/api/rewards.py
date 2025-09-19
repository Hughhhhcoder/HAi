from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.reward import Reward

router = APIRouter(prefix="/rewards", tags=["rewards"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 查询当前积分
@router.get("/points")
def get_points(user_id: int, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward:
        return {"points": 0}
    return {"points": reward.points}

# 查询奖励历史
@router.get("/history")
def get_reward_history(user_id: int, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.user_id == user_id).first()
    if not reward or not reward.reward_history:
        return []
    return [h for h in reward.reward_history.strip(",").split(",") if h] 