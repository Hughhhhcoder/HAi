from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, username: str, password: str, email: str = None):
    # 检查用户名是否已存在
    user = db.query(User).filter(User.username == username).first()
    if user:
        return None  # 用户已存在
    
    # 检查邮箱是否已存在
    if email:
        email_exists = db.query(User).filter(User.email == email).first()
        if email_exists:
            return None  # 邮箱已存在
    
    hashed = get_password_hash(password)
    new_user = User(username=username, password_hash=hashed, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user 