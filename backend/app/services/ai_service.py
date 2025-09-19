from sqlalchemy.orm import Session
from app.models.ai_role import AIRole
from app.core.database import redis_client
import requests
import os
import json
import random
from datetime import datetime

# vveai API 配置
VVEAI_API_URL = os.getenv("VVEAI_API_URL", "https://api.vveai.com/panel/token")
VVEAI_API_KEY = os.getenv("VVEAI_API_KEY", "test-key")

# Mock 回复模板
MOCK_REPLIES = {
    "温柔心理师": [
        "我理解你现在的感受。让我们一起来分析一下这个情况...",
        "这确实是一个令人困扰的问题。不过别担心，我们可以一步步来...",
        "你说得对，这种感觉很正常。让我们先从小的改变开始...",
        "听你这么说，我能感受到你的困扰。让我们换个角度思考...",
    ],
    "元气生活教练": [
        "太棒了！让我们一起制定一个充满活力的计划！",
        "这个想法不错！我建议你可以这样做...",
        "加油！改变总是从第一步开始。我来帮你规划...",
        "你已经迈出了重要的一步！接下来我们可以...",
    ]
}

# 角色管理

def get_all_roles(db: Session):
    """获取所有可用的 AI 角色"""
    return db.query(AIRole).all()

def get_role_by_id(db: Session, role_id: int):
    """根据 ID 获取角色信息"""
    return db.query(AIRole).filter(AIRole.id == role_id).first()

def save_conversation(db: Session, user_id: int, role_id: int, message: str, is_user: bool = True, image_url: str = None, audio_url: str = None):
    """保存对话记录到数据库"""
    from app.models.conversation import Conversation
    conv = Conversation(
        user_id=user_id,
        role_id=role_id,
        message=message,
        is_user=is_user,
        image_url=image_url,
        audio_url=audio_url
    )
    db.add(conv)
    db.commit()
    return conv

def get_conversation_history(db: Session, user_id: int, role_id: int, limit: int = 10):
    """获取最近的对话历史"""
    from app.models.conversation import Conversation
    return db.query(Conversation)\
        .filter(Conversation.user_id == user_id)\
        .filter(Conversation.role_id == role_id)\
        .order_by(Conversation.created_at.desc())\
        .limit(limit)\
        .all()

def mock_ai_reply(role_name: str, user_msg: str) -> str:
    """生成 mock AI 回复"""
    # 获取角色对应的回复模板
    replies = MOCK_REPLIES.get(role_name, MOCK_REPLIES["温柔心理师"])
    
    # 随机选择一个回复模板
    base_reply = random.choice(replies)
    
    # 根据用户输入适当调整回复
    if "难过" in user_msg or "伤心" in user_msg:
        return f"{base_reply} 我注意到你现在心情不太好，让我们先聊聊是什么让你感到难过..."
    elif "焦虑" in user_msg or "压力" in user_msg:
        return f"{base_reply} 压力和焦虑是很常见的，我们可以一起学习一些减压的方法..."
    elif "开心" in user_msg or "高兴" in user_msg:
        return f"{base_reply} 很高兴听到你有这样的好心情！让我们想想如何保持这种状态..."
    else:
        return base_reply

def chat_with_ai(db: Session, user_id: int, role_id: int, user_msg: str, image_url: str = None, audio_url: str = None):
    """AI 对话主函数，支持图片和语音"""
    # 获取角色信息
    role = get_role_by_id(db, role_id)
    if not role:
        return {"error": "角色不存在"}
    # 保存用户消息
    save_conversation(db, user_id, role_id, user_msg, is_user=True, image_url=image_url, audio_url=audio_url)
    # 生成 AI 回复
    ai_reply = mock_ai_reply(role.role_name, user_msg)
    if image_url:
        ai_reply += f"\n（我看到了你发的图片，真有趣！如果你想聊聊图片内容，可以告诉我~）"
    if audio_url:
        ai_reply += f"\n（我听到了你的语音，虽然我现在只能用文字回复你，但很乐意听你分享~）"
    # 保存 AI 回复
    save_conversation(db, user_id, role_id, ai_reply, is_user=False)
    return {
        "role_name": role.role_name,
        "reply": ai_reply,
        "timestamp": datetime.now().isoformat()
    }

# 会话上下文管理
REDIS_CHAT_PREFIX = "chatctx:"

# 获取上下文

def get_chat_context(user_id: int, role_id: int, max_length=10):
    key = f"{REDIS_CHAT_PREFIX}{user_id}:{role_id}"
    ctx = redis_client.lrange(key, 0, -1)
    return ctx[-max_length:] if ctx else []

# 存储对话

def append_chat_context(user_id: int, role_id: int, msg: str, max_length=10):
    key = f"{REDIS_CHAT_PREFIX}{user_id}:{role_id}"
    redis_client.rpush(key, msg)
    redis_client.ltrim(key, -max_length, -1)
    redis_client.expire(key, 60*60*24)  # 24小时过期

# vveai API 调用（可mock）
def call_vveai_api(prompt: str, user_id: int, role: AIRole):
    # 实际调用
    try:
        resp = requests.post(VVEAI_API_URL, json={
            "prompt": prompt,
            "user_id": user_id,
            "role": role.role_name,
            "api_key": VVEAI_API_KEY
        }, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("reply", "[无回复]")
        else:
            return f"[API错误] {resp.status_code}"
    except Exception as e:
        return f"[API异常] {e}"

# 组装 prompt

def build_prompt(role: AIRole, context: list, user_msg: str):
    ctx = "\n".join(context)
    return role.prompt_template.replace("{context}", ctx).replace("{user_msg}", user_msg) 