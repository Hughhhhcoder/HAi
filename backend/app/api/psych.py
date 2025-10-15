from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.psych_test import PsychTest
from app.core.psych_questionnaires import QUESTIONNAIRES, get_test_categories
import json
from datetime import datetime

router = APIRouter(prefix="/psych", tags=["psych"])

# 依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    user_id = payload.user_id
    test_type = payload.test_type
    answers = payload.answers
    
    if test_type not in QUESTIONNAIRES:
        raise HTTPException(status_code=400, detail="不支持的问卷类型")
    
    config = QUESTIONNAIRES[test_type]
    questions = config["questions"]
    
    if len(answers) != len(questions):
        raise HTTPException(status_code=400, detail="答案数量与题目数量不符")
    
    # 计算分数
    result = calculate_score(test_type, answers, config)
    
    # 生成建议
    suggestion = get_suggestion(test_type, result, config)
    
    # 存储
    record = PsychTest(
        user_id=user_id,
        test_type=test_type,
        answers_json=json.dumps(answers, ensure_ascii=False),
        score=result.get("total_score", 0),
        result_json=json.dumps(result, ensure_ascii=False)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {
        "score": result.get("total_score", 0),
        "subscores": result.get("subscores", {}),
        "suggestion": suggestion,
        "level": result.get("level", ""),
        "color": result.get("color", "green"),
        "record_id": record.id
    }

# 查询历史
@router.get("/history")
def get_psych_history(user_id: int, test_type: str = None, db: Session = Depends(get_db)):
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
            "answers": json.loads(r.answers_json)
        }
        # 如果有result_json，也返回
        if r.result_json:
            item["result"] = json.loads(r.result_json)
        result_list.append(item)
    
    return result_list

# ==================== 评分逻辑 ====================

def calculate_score(test_type: str, answers: list[int], config: dict) -> dict:
    """
    计算测评分数
    支持多种计分方式：sum（总分）、average（平均分）、subscale（分量表）
    """
    scoring_type = config.get("scoring_type", "sum")
    reverse_items = config.get("reverse_items", [])
    
    # 处理反向计分（先转换答案）
    processed_answers = []
    for i, ans in enumerate(answers):
        if i in reverse_items:
            # 反向计分：根据选项数量决定反转方式
            max_score = max([opt["score"] for opt in config["options"]])
            min_score = min([opt["score"] for opt in config["options"]])
            reversed_score = max_score + min_score - ans
            processed_answers.append(reversed_score)
        else:
            processed_answers.append(ans)
    
    result = {}
    
    if scoring_type == "sum":
        # 简单求和
        total = sum(processed_answers)
        result["total_score"] = total
        
        # 查找对应的等级和颜色
        for range_info in config["interpretation"]["ranges"]:
            if range_info["min"] <= total <= range_info["max"]:
                result["level"] = range_info["level"]
                result["color"] = range_info["color"]
                result["advice"] = range_info["advice"]
                break
    
    elif scoring_type == "average":
        # 平均分
        avg = sum(processed_answers) / len(processed_answers)
        result["total_score"] = round(avg, 2)
        
        # 查找对应的等级和颜色
        for range_info in config["interpretation"]["ranges"]:
            if range_info["min"] <= avg <= range_info["max"]:
                result["level"] = range_info["level"]
                result["color"] = range_info["color"]
                result["advice"] = range_info["advice"]
                break
    
    elif scoring_type == "subscale":
        # 分量表计分
        subscales = config["subscales"]
        subscores = {}
        
        for sub_key, sub_info in subscales.items():
            sub_items = sub_info["items"]
            sub_answers = [processed_answers[i] for i in sub_items]
            sub_total = sum(sub_answers)
            subscores[sub_key] = {
                "name": sub_info["name"],
                "score": sub_total
            }
            
            # 查找该分量表的等级
            if sub_key in config["interpretation"]:
                for range_info in config["interpretation"][sub_key]:
                    if range_info["min"] <= sub_total <= range_info["max"]:
                        subscores[sub_key]["level"] = range_info["level"]
                        subscores[sub_key]["color"] = range_info["color"]
                        subscores[sub_key]["advice"] = range_info["advice"]
                        break
        
        result["subscores"] = subscores
        result["total_score"] = sum([s["score"] for s in subscores.values()])
    
    return result

def get_suggestion(test_type: str, result: dict, config: dict) -> str:
    """
    生成专业建议
    """
    scoring_type = config.get("scoring_type", "sum")
    
    if scoring_type in ["sum", "average"]:
        # 单一分数的建议
        return result.get("advice", "测评完成。")
    
    elif scoring_type == "subscale":
        # 分量表的综合建议
        subscores = result.get("subscores", {})
        suggestions = []
        
        for sub_key, sub_data in subscores.items():
            suggestions.append(f"【{sub_data['name']}】{sub_data.get('level', '')}（{sub_data['score']}分）：{sub_data.get('advice', '')}")
        
        return "\n\n".join(suggestions)
    
    return "测评完成。"
