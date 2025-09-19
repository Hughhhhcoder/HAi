from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.schemas.ai_role import AIRoleOut
from app.services.ai_service import (
    get_all_roles, get_conversation_history, chat_with_ai
)
from app.models.ai_role import AIRole

router = APIRouter(prefix="/ai", tags=["ai"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/roles", response_model=List[AIRoleOut])
def list_roles(
    skip: int = Query(0, description="分页起始位置"),
    limit: int = Query(10, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取所有可用的 AI 角色列表"""
    roles = get_all_roles(db)
    return roles[skip : skip + limit]

@router.post("/chat")
def chat(
    user_id: int,
    role_id: int,
    message: str = "",
    image_url: str = None,
    audio_url: str = None,
    db: Session = Depends(get_db)
):
    """与 AI 角色对话，支持图片和语音
    - user_id: 用户ID
    - role_id: AI角色ID
    - message: 用户消息内容
    - image_url: 图片URL（可选）
    - audio_url: 音频URL（可选）
    """
    result = chat_with_ai(db, user_id, role_id, message, image_url, audio_url)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/history")
def get_history(
    user_id: int,
    role_id: int,
    limit: int = Query(10, description="返回最近的消息数量"),
    db: Session = Depends(get_db)
):
    """获取与特定 AI 角色的对话历史
    
    - user_id: 用户ID
    - role_id: AI角色ID
    - limit: 返回最近的消息数量
    """
    history = get_conversation_history(db, user_id, role_id, limit)
    return [{
        "message": conv.message,
        "is_user": conv.is_user,
        "timestamp": conv.created_at.isoformat()
    } for conv in history] 