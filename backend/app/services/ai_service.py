from sqlalchemy.orm import Session
from app.models.ai_role import AIRole
from app.core.database import redis_client
from app.services.memory_service import get_user_profile_summary, extract_insights_from_conversation
import requests
import os
import json
import random
from datetime import datetime

# 外部大模型 API 配置（兼容 OpenAI 风格）
AI_API_URL = os.getenv("AI_API_URL", "https://api.gpt.ge/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
AI_TOP_P = float(os.getenv("AI_TOP_P", "1"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "512"))
# 图片输入模式占位：data_url | https（当前逻辑仍优先 data_url，不改变行为）
AI_IMAGE_INPUT_MODE = os.getenv("AI_IMAGE_INPUT_MODE", "data_url").lower()
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

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

def chat_with_ai(db: Session, user_id: int, role_id: int, user_msg: str, image_url: str = None, audio_url: str = None, image_data_url: str | None = None):
    """
    AI 对话主函数，支持图片和语音。
    - 读取 Redis 上下文，拼装 prompt（若启用外部接口）
    - 整合用户画像和长期记忆
    - 保存用户消息与 AI 回复至数据库
    - 同步将新消息写入 Redis，用于短期上下文（默认 24h 过期）
    - 提取洞察更新用户记忆
    """
    role = get_role_by_id(db, role_id)
    if not role:
        return {"error": "角色不存在"}

    # 保存用户消息
    save_conversation(db, user_id, role_id, user_msg, is_user=True, image_url=image_url, audio_url=audio_url)
    append_chat_context(user_id, role_id, f"USER: {user_msg}")

    # 选择生成策略：外部 API 或 mock
    use_external = os.getenv("AI_USE_EXTERNAL", "false").lower() in ["1", "true", "yes"]
    if use_external:
        context = get_chat_context(user_id, role_id, max_length=10)
        # 获取用户画像（让 AI 了解用户）
        user_profile = get_user_profile_summary(db, user_id)
        
        # 选择图片入参策略：data_url | https（默认 data_url）
        img = None
        if AI_IMAGE_INPUT_MODE == "https":
            img = image_url
        else:
            img = image_data_url or image_url
        # 若为相对路径且设置了 PUBLIC_BASE_URL，则补全为绝对 URL
        if isinstance(img, str) and img.startswith("/") and PUBLIC_BASE_URL:
            img = f"{PUBLIC_BASE_URL}{img}"
        
        # 调用 AI API，传入用户画像
        ai_reply = call_external_chat_api(role, context, user_msg, user_profile=user_profile, image_url=img, audio_url=audio_url)
    else:
        ai_reply = mock_ai_reply(role.role_name, user_msg)

    if image_url:
        ai_reply += "\n（我看到了你发的图片，若你愿意，可以描述它带给你的感受。）"
    if audio_url:
        ai_reply += "\n（我听到了你的语音，谢谢分享。我会用文字继续回复你。）"

    # 保存 AI 回复
    save_conversation(db, user_id, role_id, ai_reply, is_user=False)
    append_chat_context(user_id, role_id, f"ASSISTANT: {ai_reply}")
    
    # 从对话中提取洞察并更新用户记忆
    try:
        extract_insights_from_conversation(db, user_id, role_id, user_msg, ai_reply)
    except Exception as e:
        print(f"[WARN] 提取洞察失败: {e}")

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

def clear_conversation(db: Session, user_id: int, role_id: int):
    """
    清空与特定角色的对话：
    - 删除数据库消息
    - 清理 Redis 上下文
    """
    from app.models.conversation import Conversation
    db.query(Conversation).filter(Conversation.user_id == user_id, Conversation.role_id == role_id).delete()
    db.commit()
    key = f"{REDIS_CHAT_PREFIX}{user_id}:{role_id}"
    try:
        redis_client.delete(key)
    except Exception:
        # 忽略 Redis 清理失败
        pass

def _build_messages_from_context(role: AIRole, context: list[str], user_msg: str, user_profile: str = "", image_url: str | None = None) -> list:
    messages = []
    # 系统提示词：使用角色模板并注入用户画像和上下文
    if role and role.prompt_template:
        # 构建对话历史字符串
        context_str = "\n".join(context) if context else "（无对话历史）"
        
        # 将用户画像、上下文、用户消息注入模板
        system_prompt = role.prompt_template.format(
            user_profile=user_profile or "（暂无用户画像信息）",
            context=context_str,
            user_msg="{placeholder}"  # 占位符，实际消息在 user message 中
        )
        # 移除占位符
        system_prompt = system_prompt.replace("{placeholder}", "")
        
        messages.append({"role": "system", "content": system_prompt})

    # 注意：上下文已经在系统提示词中，这里不重复添加
    # OpenAI API 会根据系统提示词理解对话历史

    # 当前用户消息（支持图片）
    if image_url:
        # 使用多模态内容：text + image_url
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_msg or ""},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        })
    else:
        messages.append({"role": "user", "content": user_msg})

    return messages

def call_external_chat_api(role: AIRole, context: list[str], user_msg: str, user_profile: str = "", image_url: str | None = None, audio_url: str | None = None) -> str:
    """调用外部对话接口（OpenAI 风格），返回字符串。带简单退避重试。"""
    if not AI_API_KEY or not AI_API_URL:
        return "[配置缺失] 请设置 AI_API_KEY 与 AI_API_URL 后再试"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = _build_messages_from_context(role, context, user_msg, user_profile, image_url)

    def make_payload(msgs):
        return {
            "model": AI_MODEL,
            "messages": msgs,
            "temperature": AI_TEMPERATURE,
            "top_p": AI_TOP_P,
            "max_tokens": AI_MAX_TOKENS,
            "stream": False,
        }

    payload = make_payload(messages)

    # 若有音频但对方暂不支持，退化为文本说明
    if audio_url and not image_url:
        # 附加一条说明文本
        payload["messages"].append({"role": "user", "content": f"音频链接: {audio_url}"})

    backoff = 1
    for _ in range(3):
        try:
            resp = requests.post(AI_API_URL, headers=headers, data=json.dumps(payload), timeout=45)
            if resp.status_code == 200:
                data = resp.json()
                try:
                    content = data["choices"][0]["message"]["content"]
                except Exception:
                    content = data.get("reply") or json.dumps(data, ensure_ascii=False)
                return content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
            elif resp.status_code in (429, 500, 502, 503, 504):
                # 退避重试
                import time
                time.sleep(backoff)
                backoff = min(backoff * 2, 4)
                continue
            elif resp.status_code in (400, 404) and image_url:
                # 多模态可能不被支持：把图片 URL 拼入文本退化再试
                text_only_messages = _build_messages_from_context(role, context, f"[图片链接] {image_url}\n{user_msg}", None)
                resp2 = requests.post(AI_API_URL, headers=headers, data=json.dumps(make_payload(text_only_messages)), timeout=45)
                if resp2.status_code == 200:
                    data = resp2.json()
                    try:
                        content = data["choices"][0]["message"]["content"]
                    except Exception:
                        content = data.get("reply") or json.dumps(data, ensure_ascii=False)
                    return content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
            elif resp.status_code in (413, 422):
                # 体积/格式问题：返回更友好的提示
                hint = "请求体过大或格式不被支持。若包含图片，请尝试降低分辨率/文件大小，或改用 https 公网 URL。"
                try:
                    err = resp.json()
                    msg = err.get("error", {}).get("message") or err.get("message") or str(err)
                except Exception:
                    msg = resp.text
                return f"[API错误 {resp.status_code}] {msg}｜{hint}"
            else:
                # 返回错误详情
                try:
                    err = resp.json()
                    msg = err.get("error", {}).get("message") or err.get("message") or str(err)
                except Exception:
                    msg = resp.text
                return f"[API错误 {resp.status_code}] {msg}"
        except Exception as e:
            last_err = str(e)
            import time
            time.sleep(backoff)
            backoff = min(backoff * 2, 4)
            continue

    return f"[API异常] 请求失败，请稍后再试"

def call_external_chat_api_stream(role: AIRole, context: list[str], user_msg: str, user_profile: str = "", image_url: str | None = None):
    """生成器：以 SSE 形式逐段产出文本片段（纯字符串）。"""
    if not AI_API_KEY or not AI_API_URL:
        yield "配置缺失，请设置 AI_API_KEY 与 AI_API_URL"
        return

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    messages = _build_messages_from_context(role, context, user_msg, user_profile, image_url)

    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "temperature": AI_TEMPERATURE,
        "top_p": AI_TOP_P,
        "max_tokens": AI_MAX_TOKENS,
        "stream": True,
    }

    try:
        with requests.post(AI_API_URL, headers=headers, data=json.dumps(payload), timeout=60, stream=True) as resp:
            if resp.status_code != 200:
                try:
                    err = resp.json()
                    msg = err.get("error", {}).get("message") or err.get("message") or str(err)
                except Exception:
                    msg = resp.text
                yield f"[API错误 {resp.status_code}] {msg}"
                return
            for raw_line in resp.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                line = raw_line.strip()
                if not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                # OpenAI 风格：{"choices":[{"delta":{"content":"字"}}]}
                try:
                    j = json.loads(data)
                    delta = j.get("choices", [{}])[0].get("delta", {}).get("content")
                    if isinstance(delta, str) and delta:
                        yield delta
                except Exception:
                    # 若不是标准 JSON，就直接回传
                    if data:
                        yield data
    except Exception as e:
        yield f"[API异常] {e}"

# 组装 prompt

def build_prompt(role: AIRole, context: list, user_msg: str):
    ctx = "\n".join(context)
    return role.prompt_template.replace("{context}", ctx).replace("{user_msg}", user_msg) 