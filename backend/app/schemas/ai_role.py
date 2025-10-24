from pydantic import BaseModel
from typing import Optional

class AIRoleOut(BaseModel):
    id: int
    role_name: str
    description: Optional[str] = None  # 用户可见的描述
    emoji: Optional[str] = None  # 角色图标
    tags: Optional[str] = None  # 标签
    gradient: Optional[str] = None  # 渐变色彩
    # prompt_template 不返回给前端，保护内部提示词

    class Config:
        orm_mode = True 