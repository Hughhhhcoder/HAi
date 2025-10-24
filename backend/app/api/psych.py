"""
心理测评 API
支持 10 个专业量表（完整版192题）
集成 AI 报告生成和用户画像实时更新
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.psych_test import PsychTest
from app.core.psych_questionnaires import QUESTIONNAIRES, get_test_categories, calculate_score_and_suggestion
from app.services.report_service import generate_assessment_report
from app.services.memory_service import update_profile_with_psych_test
from app.models.user_memory import UserInsight
import json
from datetime import datetime

router = APIRouter(prefix="/api/psych", tags=["psych"])


# 获取所有测评分类和列表
@router.get("/categories")
def get_all_categories():
    """获取所有测评分类及其下的量表列表"""
    return get_test_categories()


# 获取问卷题目
@router.get("/questionnaire")
def get_questionnaire(test_type: str):
    """获取指定量表的完整信息"""
    if test_type not in QUESTIONNAIRES:
        raise HTTPException(status_code=400, detail="不支持的问卷类型")
    
    config = QUESTIONNAIRES[test_type]
    return {
        "title": config["title"],
        "abbr": config["abbr"],
        "category": config["category"],
        "description": config["description"],
        "time": config["time"],
        "questions": config["questions"],
        "options": config["options"]
    }


# 提交测评
class PsychSubmit(BaseModel):
    user_id: int
    test_type: str
    answers: list[int]


@router.post("/submit")
def submit_psych_test(payload: PsychSubmit, db: Session = Depends(get_db)):
    """
    提交心理测评，自动生成 AI 专业报告并更新用户画像
    """
    user_id = payload.user_id
    test_type = payload.test_type
    answers = payload.answers
    
    if test_type not in QUESTIONNAIRES:
        raise HTTPException(status_code=400, detail="不支持的问卷类型")
    
    config = QUESTIONNAIRES[test_type]
    questions = config["questions"]
    
    if len(answers) != len(questions):
        raise HTTPException(status_code=400, detail="答案数量与题目数量不符")
    
    # 1. 计算分数和基础建议（使用统一的评分引擎）
    score, result_details = calculate_score_and_suggestion(test_type, answers)
    
    # 2. 调用 AI 生成专业评估报告
    print(f"[INFO] 开始为用户 {user_id} 生成 {test_type} 的 AI 专业报告...")
    ai_report = generate_assessment_report(test_type, score, result_details, user_id)
    
    # 3. 存储到数据库
    record = PsychTest(
        user_id=user_id,
        test_type=test_type,
        answers_json=json.dumps(answers, ensure_ascii=False),
        score=score,
        result_json=json.dumps(result_details, ensure_ascii=False),
        ai_report=ai_report  # 新增：存储 AI 报告
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    # 4. 更新用户画像（实时同步测评结果）
    try:
        update_profile_with_psych_test(db, user_id, test_type, score, result_details)
        print(f"[INFO] 已将 {test_type} 测评结果同步到用户 {user_id} 的画像")
    except Exception as e:
        print(f"[WARN] 更新用户画像失败: {e}")
    
    # 5. 返回完整结果
    return {
        "record_id": record.id,
        "score": score,
        "result_details": result_details,
        "ai_report": ai_report,  # 新增：返回 AI 报告
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None
    }


# 查询历史
@router.get("/history")
def get_psych_history(user_id: int, test_type: str = None, db: Session = Depends(get_db)):
    """获取心理测评历史记录，包含 AI 报告"""
    q = db.query(PsychTest).filter(PsychTest.user_id == user_id)
    if test_type:
        q = q.filter(PsychTest.test_type == test_type)
    records = q.order_by(PsychTest.date.desc()).all()
    
    result_list = []
    for r in records:
        item = {
            "id": r.id,
            "test_type": r.test_type,
            "score": r.score,
            "date": r.date,
            "answers": json.loads(r.answers_json) if r.answers_json else [],
            "result_details": json.loads(r.result_json) if r.result_json else {},
            "ai_report": r.ai_report,  # 新增：返回 AI 报告
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None
        }
        result_list.append(item)
    
    return result_list


# 获取单个测评详情（包含完整 AI 报告）
@router.get("/report/{record_id}")
def get_test_report(record_id: int, db: Session = Depends(get_db)):
    """获取测评的完整报告，包含 AI 专业解读"""
    record = db.query(PsychTest).filter(PsychTest.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="测评记录不存在")
    
    result_details = json.loads(record.result_json) if record.result_json else {}
    
    return {
        "id": record.id,
        "test_type": record.test_type,
        "score": record.score,
        "date": record.date,
        "result_details": result_details,
        "ai_report": record.ai_report
    }


# 获取用户画像
@router.get("/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """获取用户心理画像，包含测评结果和AI洞察"""
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    
    if not insight:
        return {
            "user_id": user_id,
            "main_concerns": "",
            "strengths": "",
            "coping_patterns": "",
            "core_traits": "",
            "triggers": "",
            "summary": ""
        }
    
    return {
        "user_id": user_id,
        "main_concerns": insight.main_concerns or "",
        "strengths": insight.strengths or "",
        "coping_patterns": insight.coping_patterns or "",
        "core_traits": insight.core_traits or "",
        "triggers": insight.triggers or "",
        "summary": insight.summary or "",
        "created_at": insight.created_at.isoformat() if insight.created_at else None,
        "updated_at": insight.updated_at.isoformat() if insight.updated_at else None,
        "last_profile_update": insight.last_profile_update.isoformat() if insight.last_profile_update else None
    }
