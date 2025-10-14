"""
专业知识管理 API
用于查看和管理心理学专业知识库
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.psychology_knowledge import PsychologyKnowledge, KnowledgeUsageLog
from app.services.knowledge_service import add_knowledge
from typing import List

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


@router.get("/list")
def list_knowledge(
    category: str = None,
    subcategory: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取知识列表"""
    query = db.query(PsychologyKnowledge)
    
    if category:
        query = query.filter(PsychologyKnowledge.category == category)
    if subcategory:
        query = query.filter(PsychologyKnowledge.subcategory == subcategory)
    
    knowledge_list = query.order_by(
        PsychologyKnowledge.reliability_score.desc(),
        PsychologyKnowledge.usage_count.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": k.id,
            "title": k.title,
            "category": k.category,
            "subcategory": k.subcategory,
            "content": k.content[:200] + "..." if len(k.content) > 200 else k.content,
            "keywords": k.keywords,
            "source": k.source,
            "reliability_score": k.reliability_score,
            "usage_count": k.usage_count
        }
        for k in knowledge_list
    ]


@router.get("/detail/{knowledge_id}")
def get_knowledge_detail(knowledge_id: int, db: Session = Depends(get_db)):
    """获取知识详情"""
    knowledge = db.query(PsychologyKnowledge).filter(PsychologyKnowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="知识不存在")
    
    return {
        "id": knowledge.id,
        "title": knowledge.title,
        "category": knowledge.category,
        "subcategory": knowledge.subcategory,
        "content": knowledge.content,
        "keywords": knowledge.keywords,
        "source": knowledge.source,
        "reliability_score": knowledge.reliability_score,
        "usage_count": knowledge.usage_count,
        "created_at": knowledge.created_at,
        "updated_at": knowledge.updated_at
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """获取所有知识分类"""
    categories = db.query(PsychologyKnowledge.category, PsychologyKnowledge.subcategory)\
        .distinct().all()
    
    result = {}
    for cat, subcat in categories:
        if cat not in result:
            result[cat] = set()
        if subcat:
            result[cat].add(subcat)
    
    return {cat: list(subcats) for cat, subcats in result.items()}


@router.get("/stats")
def get_knowledge_stats(db: Session = Depends(get_db)):
    """获取知识库统计信息"""
    total_knowledge = db.query(PsychologyKnowledge).count()
    total_usage = db.query(KnowledgeUsageLog).count()
    
    category_stats = db.query(
        PsychologyKnowledge.category,
        func.count(PsychologyKnowledge.id)
    ).group_by(PsychologyKnowledge.category).all()
    
    return {
        "total_knowledge": total_knowledge,
        "total_usage": total_usage,
        "category_stats": {cat: count for cat, count in category_stats}
    }


@router.post("/add")
def add_new_knowledge(
    title: str,
    category: str,
    content: str,
    subcategory: str = None,
    keywords: str = None,
    source: str = None,
    reliability_score: int = 8,
    db: Session = Depends(get_db)
):
    """添加新知识（管理员功能）"""
    knowledge = add_knowledge(
        db=db,
        title=title,
        category=category,
        content=content,
        subcategory=subcategory,
        keywords=keywords,
        source=source,
        reliability_score=reliability_score
    )
    
    return {
        "msg": "知识添加成功",
        "knowledge_id": knowledge.id,
        "title": knowledge.title
    }

