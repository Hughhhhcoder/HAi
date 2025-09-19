from pydantic import BaseModel

class AIRoleOut(BaseModel):
    id: int
    role_name: str
    prompt_template: str

    class Config:
        orm_mode = True 