from fastapi import APIRouter, Depends, HTTPException, Query, Form, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.schemas.ai_role import AIRoleOut
from app.services.ai_service import (
    get_all_roles, get_conversation_history, chat_with_ai, clear_conversation,
    get_chat_context, append_chat_context, mock_ai_reply, get_role_by_id,
    call_external_chat_api_stream, call_external_chat_api, save_conversation
)
from app.models.ai_role import AIRole

router = APIRouter(prefix="/api/ai", tags=["ai"])

class ChatRequest(BaseModel):
    user_id: int
    role_id: int
    message: str = ""
    image_url: Optional[str] = None
    image_data_url: Optional[str] = None
    audio_url: Optional[str] = None

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
async def chat(
    request: Request,
    db: Session = Depends(get_db)
):
    """与 AI 角色对话，支持图片和语音。允许 JSON 或 Form 提交。"""
    payload = {}
    try:
        payload = await request.json()
        print(f"[DEBUG] JSON payload: {payload}")
    except Exception as e:
        print(f"[DEBUG] JSON parse failed: {e}")
        try:
            form = await request.form()
            payload = dict(form)
            print(f"[DEBUG] Form payload: {payload}")
        except Exception as e2:
            print(f"[DEBUG] Form parse failed: {e2}")
            payload = {}

    # 容错解析与类型转换
    def to_int(v):
        try:
            return int(v)
        except Exception:
            return None

    user_id = to_int(payload.get("user_id"))
    role_id = to_int(payload.get("role_id"))
    message = (payload.get("message") or "").strip()
    image_url = payload.get("image_url")
    image_data_url = payload.get("image_data_url")
    audio_url = payload.get("audio_url")

    print(f"[DEBUG] Parsed: user_id={user_id}, role_id={role_id}, message='{message}'")

    if user_id is None or role_id is None:
        print(f"[DEBUG] Validation failed: user_id={user_id}, role_id={role_id}")
        raise HTTPException(status_code=422, detail=f"user_id 与 role_id 为必填整数，收到: user_id={user_id}, role_id={role_id}")

    result = chat_with_ai(db, user_id, role_id, message, image_url, audio_url, image_data_url=image_data_url)
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
        "timestamp": conv.created_at.isoformat(),
        "image_url": conv.image_url,
        "audio_url": conv.audio_url
    } for conv in history]

@router.get("/full-history")
def get_full_history(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    """获取与特定 AI 角色的完整对话历史（长期记忆）
    
    - user_id: 用户ID
    - role_id: AI角色ID
    """
    history = get_conversation_history(db, user_id, role_id, limit=1000)  # 获取所有历史记录
    return {
        "total_messages": len(history),
        "conversations": [{
            "id": conv.id,
            "message": conv.message,
            "is_user": conv.is_user,
            "timestamp": conv.created_at.isoformat(),
            "image_url": conv.image_url,
            "audio_url": conv.audio_url
        } for conv in history]
    } 

@router.post("/clear")
def clear_history(
    user_id: int = Form(...),
    role_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """清空与某个 AI 角色的历史记录与上下文"""
    clear_conversation(db, user_id, role_id)
    return {"msg": "已清空对话历史"}

@router.post("/stream")
def stream_chat(
    user_id: int = Form(...),
    role_id: int = Form(...),
    message: str = Form(""),
    image_url: str | None = Form(None),
    db: Session = Depends(get_db)
):
    """SSE 实时输出 AI 回复（推荐用于外部模型）。"""

    role = get_role_by_id(db, role_id)
    if not role:
        def err_gen():
            yield "data: 角色不存在\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(err_gen(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        })

    # 保存用户消息并写入上下文
    save_conversation(db, user_id, role_id, message, is_user=True, image_url=image_url)
    append_chat_context(user_id, role_id, f"USER: {message}")

    use_external = os.getenv("AI_USE_EXTERNAL", "false").lower() in ["1", "true", "yes"]
    context = get_chat_context(user_id, role_id, max_length=10)

    def event_generator():
        full_reply = ""
        emitted = False
        try:
            if use_external:
                chunks = call_external_chat_api_stream(role, context, message, image_url=image_url)
                for ch in chunks:
                    text = str(ch)
                    if not text:
                        continue
                    full_reply += text
                    yield f"data: {text}\n\n"
                    emitted = True
            else:
                # 本地 mock 的流式回放
                import time
                reply = mock_ai_reply(role.role_name, message)
                for ch in reply:
                    full_reply += ch
                    yield f"data: {ch}\n\n"
                    time.sleep(0.02)
                    emitted = True
            # 若外部未产出流式片段，则退化为非流式一次性调用并逐字回放
            if use_external and not emitted:
                import time
                reply = call_external_chat_api(role, context, message, image_url=image_url)
                for ch in str(reply):
                    full_reply += ch
                    yield f"data: {ch}\n\n"
                    time.sleep(0.02)
        finally:
            # 结束时保存 AI 回复与上下文
            if full_reply:
                save_conversation(db, user_id, role_id, full_reply, is_user=False)
                append_chat_context(user_id, role_id, f"ASSISTANT: {full_reply}")
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    })