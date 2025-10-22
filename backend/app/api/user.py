from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.core.database import SessionLocal

router = APIRouter(prefix="/api/user", tags=["user"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.username, user.password, user.email)
    if not new_user:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    return {"msg": "注册成功", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"msg": "登录成功", "user_id": auth_user.id} 