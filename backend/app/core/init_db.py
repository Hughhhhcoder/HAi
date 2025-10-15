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
from app.models.user_memory import UserMemory, UserInsight
from app.models.psychology_knowledge import PsychologyKnowledge, KnowledgeUsageLog
from app.services.user_service import create_user
from app.services.knowledge_service import add_knowledge, link_knowledge_to_role
from app.core.psychology_roles import PSYCHOLOGY_AI_ROLES
from app.core.psychology_knowledge_data import PSYCHOLOGY_KNOWLEDGE_DATA, get_role_knowledge_mapping

def init_db():
    print("[INFO] 开始初始化数据库...")
    
    # 确保所有模型都被注册到 Base.metadata
    all_models = [User, AIRole, UserMemory, UserInsight, PsychologyKnowledge, KnowledgeUsageLog]
    print(f"[INFO] 已加载模型: {[model.__name__ for model in all_models]}")
    
    print("[INFO] 创建所有表(如果不存在)...")
    Base.metadata.create_all(bind=engine)
    
    print("[INFO] 插入/更新专业心理健康 AI 角色...")
    db = SessionLocal()
    if db.query(AIRole).count() == 0:
        # 从配置文件加载 10 个专业心理角色
        roles = [
            AIRole(
                role_name=role["role_name"],
                prompt_template=role["prompt_template"]
            )
            for role in PSYCHOLOGY_AI_ROLES
        ]
        db.add_all(roles)
        db.commit()
        print(f"[INFO] 已创建 {len(roles)} 个专业心理健康 AI 角色")
    else:
        # 更新现有角色的 prompt_template
        for i, role_data in enumerate(PSYCHOLOGY_AI_ROLES, start=1):
            role = db.query(AIRole).filter(AIRole.id == i).first()
            if role:
                role.prompt_template = role_data["prompt_template"]
                print(f"[INFO] 已更新角色 {i}: {role.role_name}")
        db.commit()
        print(f"[INFO] 已更新所有角色的专业提示词")
    
    print("[INFO] 插入专业心理学知识...")
    if db.query(PsychologyKnowledge).count() == 0:
        # 加载知识数据
        knowledge_mapping = {}  # title -> knowledge object
        for kdata in PSYCHOLOGY_KNOWLEDGE_DATA:
            k = add_knowledge(
                db=db,
                title=kdata["title"],
                category=kdata["category"],
                subcategory=kdata.get("subcategory"),
                content=kdata["content"],
                keywords=kdata.get("keywords"),
                source=kdata.get("source"),
                reliability_score=kdata.get("reliability_score", 8)
            )
            knowledge_mapping[k.title] = k
        print(f"[INFO] 已创建 {len(knowledge_mapping)} 条专业知识")
        
        # 关联知识到角色
        role_knowledge_map = get_role_knowledge_mapping()
        for role_name, knowledge_list in role_knowledge_map.items():
            role = db.query(AIRole).filter(AIRole.role_name == role_name).first()
            if role:
                for k_title, priority in knowledge_list:
                    if k_title in knowledge_mapping:
                        link_knowledge_to_role(
                            db=db,
                            knowledge_id=knowledge_mapping[k_title].id,
                            role_id=role.id,
                            priority=priority
                        )
        print(f"[INFO] 已关联知识到各个角色")
    else:
        print("[INFO] 专业知识已存在，跳过")
    
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