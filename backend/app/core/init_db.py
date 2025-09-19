import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

from app.core.database import engine, Base, SessionLocal
from app.models.user import User  # 显式导入每个模型
from app.models.ai_role import AIRole
from app.models.conversation import Conversation
from app.models.user_profile import UserProfile
from app.models.recovery_plan import RecoveryPlan
from app.models.psych_test import PsychTest
from app.models.daily_checkin import DailyCheckin
from app.models.reward import Reward
from app.models.literature_file import LiteratureFile
from app.models.literature_chunk import LiteratureChunk
from app.services.user_service import create_user

def init_db():
    print("[INFO] 开始初始化数据库...")
    
    # 确保所有模型都被注册到 Base.metadata
    all_models = [User, AIRole]
    print(f"[INFO] 已加载模型: {[model.__name__ for model in all_models]}")
    
    print("[INFO] 创建所有表(如果不存在)...")
    Base.metadata.create_all(bind=engine)
    
    print("[INFO] 插入默认AI角色...")
    db = SessionLocal()
    if db.query(AIRole).count() == 0:
        db.add_all([
            AIRole(
                role_name="温柔心理师",
                prompt_template="你是温柔的心理咨询师，结合以下对话历史和用户提问，给出专业且温暖的建议。历史：{context} 用户：{user_msg}"
            ),
            AIRole(
                role_name="元气生活教练",
                prompt_template="你是充满活力的生活教练，结合以下对话历史和用户提问，给出积极、实用的生活建议。历史：{context} 用户：{user_msg}"
            )
        ])
        db.commit()
    
    print("[INFO] 创建测试用户...")
    # 创建一个测试用户方便登录测试
    test_user = create_user(db, "admin", "admin123")
    if test_user:
        print("[INFO] 测试用户创建成功 - 用户名: admin, 密码: admin123")
    else:
        print("[INFO] 测试用户已存在")
    
    db.close()
    
    print("[INFO] 数据库初始化完成！")
    print("[INFO] 可以使用以下测试账号登录：")
    print("       用户名: admin")
    print("       密码: admin123")

if __name__ == "__main__":
    init_db() 