from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import user_router, ai_router
from app.api.upload import router as upload_router
from app.api.literature import router as literature_router
from app.api.psych import router as psych_router
from app.api.plan import router as plan_router
from app.api.checkin import router as checkin_router
from app.api.rewards import router as rewards_router
from app.api.knowledge import router as knowledge_router
import os

app = FastAPI(title="Hai 后端 API")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],  # 允许前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态图片目录
static_dir = os.path.join(os.path.dirname(__file__), '../uploads/images')
static_dir = os.path.abspath(static_dir)
os.makedirs(static_dir, exist_ok=True)
app.mount("/static/images", StaticFiles(directory=static_dir), name="static_images")

# 挂载静态音频目录
static_audio_dir = os.path.join(os.path.dirname(__file__), '../uploads/audio')
static_audio_dir = os.path.abspath(static_audio_dir)
os.makedirs(static_audio_dir, exist_ok=True)
app.mount("/static/audio", StaticFiles(directory=static_audio_dir), name="static_audio")

app.include_router(user_router)
app.include_router(ai_router)
app.include_router(upload_router)
app.include_router(literature_router)
app.include_router(psych_router)
app.include_router(plan_router)
app.include_router(checkin_router)
app.include_router(rewards_router)
app.include_router(knowledge_router)

@app.get("/ping")
def ping():
    return {"msg": "pong"} 