from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.psych_test import PsychTest
import json
from datetime import datetime

router = APIRouter(prefix="/psych", tags=["psych"])

# 问卷题库
PHQ9_QUESTIONS = [
    "在过去的两周里，您感到心情郁闷、沮丧或绝望吗？",
    "在过去的两周里，您对做事失去兴趣或乐趣了吗？",
    "在过去的两周里，您入睡困难、睡不安稳或睡得过多吗？",
    "在过去的两周里，您感到疲倦或没有活力吗？",
    "在过去的两周里，您食欲不振或吃得过多吗？",
    "在过去的两周里，您觉得自己很糟糕，觉得自己让家人失望，或觉得自己是个失败者吗？",
    "在过去的两周里，您对事物专注有困难吗？",
    "在过去的两周里，您动作或说话变慢，或变得比平时更烦躁或坐立不安吗？",
    "在过去的两周里，您有想过死，或用某种方式伤害自己吗？"
]
GAD7_QUESTIONS = [
    "在过去的两周里，您感到紧张、焦虑或急躁吗？",
    "在过去的两周里，您无法停止或控制担忧吗？",
    "在过去的两周里，您对各种事情过度担忧吗？",
    "在过去的两周里，您很难放松下来吗？",
    "在过去的两周里，您感到坐立不安，难以静坐吗？",
    "在过去的两周里，您容易变得烦躁或容易生气吗？",
    "在过去的两周里，您感到害怕，好像有什么可怕的事情会发生吗？"
]
OPTIONS = [
    {"text": "完全没有", "score": 0},
    {"text": "有几天", "score": 1},
    {"text": "一半以上天数", "score": 2},
    {"text": "几乎每天", "score": 3}
]

QUESTIONNAIRES = {
    "PHQ9": {"title": "PHQ-9 抑郁自评量表", "questions": PHQ9_QUESTIONS, "options": OPTIONS},
    "GAD7": {"title": "GAD-7 焦虑自评量表", "questions": GAD7_QUESTIONS, "options": OPTIONS}
}

# 依赖

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取问卷题目
@router.get("/questionnaire")
def get_questionnaire(test_type: str):
    if test_type not in QUESTIONNAIRES:
        raise HTTPException(status_code=400, detail="不支持的问卷类型")
    return QUESTIONNAIRES[test_type]

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
    questions = QUESTIONNAIRES[test_type]["questions"]
    if len(answers) != len(questions):
        raise HTTPException(status_code=400, detail="答案数量与题目数量不符")
    score = sum(answers)
    # 生成建议
    suggestion = get_suggestion(test_type, score)
    # 存储
    record = PsychTest(
        user_id=user_id,
        test_type=test_type,
        answers_json=json.dumps(answers, ensure_ascii=False),
        score=score
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"score": score, "suggestion": suggestion, "record_id": record.id}

# 查询历史
@router.get("/history")
def get_psych_history(user_id: int, test_type: str = None, db: Session = Depends(get_db)):
    q = db.query(PsychTest).filter(PsychTest.user_id == user_id)
    if test_type:
        q = q.filter(PsychTest.test_type == test_type)
    records = q.order_by(PsychTest.date.desc()).all()
    return [{
        "id": r.id,
        "test_type": r.test_type,
        "score": r.score,
        "date": r.date,
        "answers": json.loads(r.answers_json)
    } for r in records]

# 建议生成逻辑

def get_suggestion(test_type: str, score: int) -> str:
    if test_type == "PHQ9":
        if score < 5:
            return "无抑郁症状或极轻微。建议保持良好心态。"
        elif score < 10:
            return "轻度抑郁。建议适当放松，关注自我情绪。"
        elif score < 15:
            return "中度抑郁。建议寻求心理支持，必要时咨询专业人士。"
        elif score < 20:
            return "中重度抑郁。建议尽快寻求专业心理帮助。"
        else:
            return "重度抑郁。建议立即联系专业心理医生。"
    elif test_type == "GAD7":
        if score < 5:
            return "无焦虑症状或极轻微。建议保持良好心态。"
        elif score < 10:
            return "轻度焦虑。建议适当放松，关注自我情绪。"
        elif score < 15:
            return "中度焦虑。建议寻求心理支持，必要时咨询专业人士。"
        else:
            return "重度焦虑。建议尽快寻求专业心理帮助。"
    return "--" 