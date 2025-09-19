import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.database import SessionLocal
from app.models.literature_file import LiteratureFile
from app.models.literature_chunk import LiteratureChunk
import mimetypes

router = APIRouter(prefix="/literature", tags=["literature"])

LIT_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads/literature'))
os.makedirs(LIT_UPLOAD_DIR, exist_ok=True)

CHUNK_SIZE = 400  # 每段最大字符数

# 依赖

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 文献上传
@router.post("/upload")
def upload_literature(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in ['.pdf', '.txt']:
        raise HTTPException(status_code=400, detail="只支持PDF和TXT文件")
    # 保存文件
    filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(LIT_UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # 记录元数据
    lit_file = LiteratureFile(
        filename=file.filename,
        file_path=file_path,
        file_type=ext[1:]
    )
    db.add(lit_file)
    db.commit()
    db.refresh(lit_file)
    # 解析并分段
    if ext == '.pdf':
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text = "\n".join([page.get_text() for page in doc])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF解析失败: {e}")
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    # 分段
    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    for idx, chunk in enumerate(chunks):
        db.add(LiteratureChunk(
            file_id=lit_file.id,
            chunk_index=idx,
            text=chunk,
            embedding=None  # mock
        ))
    db.commit()
    return {"file_id": lit_file.id, "filename": lit_file.filename, "chunks": len(chunks)}

# 文献列表
@router.get("/list")
def list_literature(db: Session = Depends(get_db)):
    files = db.query(LiteratureFile).order_by(LiteratureFile.upload_time.desc()).all()
    return [{
        "id": f.id,
        "filename": f.filename,
        "file_type": f.file_type,
        "upload_time": f.upload_time
    } for f in files]

# 查看某文献分段内容
@router.get("/chunks")
def get_chunks(file_id: int, db: Session = Depends(get_db)):
    chunks = db.query(LiteratureChunk).filter(LiteratureChunk.file_id == file_id).order_by(LiteratureChunk.chunk_index).all()
    return [{
        "chunk_index": c.chunk_index,
        "text": c.text
    } for c in chunks]

# 检索接口（mock相似度）
@router.get("/search")
def search_literature(query: str, top_k: int = 3, db: Session = Depends(get_db)):
    # mock: 用简单的关键词出现次数做相似度
    all_chunks = db.query(LiteratureChunk).all()
    scored = []
    for c in all_chunks:
        score = c.text.count(query)
        if score > 0:
            scored.append((score, c))
    scored.sort(reverse=True, key=lambda x: x[0])
    top_chunks = scored[:top_k]
    return [{
        "file_id": c.file_id,
        "chunk_index": c.chunk_index,
        "text": c.text,
        "score": score
    } for score, c in top_chunks] 