import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import base64
import mimetypes
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../uploads/images')
UPLOAD_DIR = os.path.abspath(UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)

AUDIO_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../uploads/audio')
AUDIO_UPLOAD_DIR = os.path.abspath(AUDIO_UPLOAD_DIR)
os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/image")
def upload_image(file: UploadFile = File(...)):
    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只支持图片文件上传")
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # 构造图片URL
    url = f"/static/images/{filename}"
    # 生成 data:URL（便于外部多模态API直接访问）
    try:
        mime, _ = mimetypes.guess_type(file_path)
        mime = mime or "image/jpeg"
        with open(file_path, "rb") as rf:
            b64 = base64.b64encode(rf.read()).decode("utf-8")
        data_url = f"data:{mime};base64,{b64}"
    except Exception:
        data_url = None
    return JSONResponse({"url": url, "data_url": data_url})

@router.post("/audio")
def upload_audio(file: UploadFile = File(...)):
    # 检查文件类型
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="只支持音频文件上传")
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(AUDIO_UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    url = f"/static/audio/{filename}"
    return JSONResponse({"url": url}) 