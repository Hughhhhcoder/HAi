# 更新日志

## 2025-10-15
- **移除文献库功能**：简化系统，专注于核心 AI 对话和心理健康支持
  - 删除后端文献相关 API (`/literature/*`)
  - 删除文献相关模型 (`LiteratureFile`, `LiteratureChunk`)
  - 删除前端文献列表页面和路由
  - 删除前端文献 API 接口
  - 保留数据库表（可选择后续手动删除）

## 2025-10-14

### 🎓 专业知识增强系统（Knowledge-Enhanced AI）
- **专业心理学知识库**：所有 AI 角色具备真实专业知识基础
  - 新增 `psychology_knowledge` 表：存储心理学理论、技术、案例、干预方法等
  - 新增 `role_knowledge_mapping` 表：角色与知识的多对多关联（含优先级）
  - 新增 `knowledge_usage_logs` 表：记录知识使用情况
  - 预置 25+ 条专业知识：涵盖 CBT、正念、积极心理学、EFT、创伤疗愈、关系治疗等
- **知识检索增强（RAG）**：AI 回复前自动检索相关专业知识
  - 基于用户消息和困扰的关键词检索
  - 角色专属知识优先（如 CBT 角色优先检索认知行为疗法知识）
  - 知识自动注入到 AI 系统提示词中
  - 追踪知识使用情况，优化检索效果
- **专业知识管理 API**：
  - `/knowledge/list`：浏览知识库
  - `/knowledge/stats`：知识库统计
  - `/knowledge/add`：添加新知识（可扩展）
- **新增文件**：
  - `backend/app/models/psychology_knowledge.py`：知识库数据模型
  - `backend/app/services/knowledge_service.py`：知识检索与管理服务
  - `backend/app/core/psychology_knowledge_data.py`：预置专业知识数据
  - `backend/app/core/add_knowledge_tables.sql`：知识表迁移脚本
  - `backend/app/api/knowledge.py`：知识管理 API
- **修改**：
  - `ai_service.py`：整合知识检索到对话流程
  - `init_db.py`：自动加载专业知识并关联到角色

### 🧠 AI 角色升级与长期记忆系统
- **AI 角色升级**：从 2 个通用角色扩展为 10 个专业心理健康 AI 角色
  - 新增专业角色：温暖倾听者·艾米、认知教练·理查德、正念导师·静心、积极心理师·阳光、情绪专家·心涟、创伤疗愈师·守护、青少年导师·星辰、职场心理顾问·行远、关系咨询师·和鸣、生命意义探索者·启明
  - 每个角色基于真实心理学流派（人本主义、CBT、正念、积极心理学、EFT 等）
  - 角色提示词包含专业背景、咨询风格、核心方法和咨询原则
- **长期记忆系统**：AI 可以逐渐了解用户
  - 新增 `user_memories` 表：存储用户性格、困扰、目标、触发因素等记忆
  - 新增 `user_insights` 表：存储用户深层洞察（核心特质、应对模式等）
  - 自动提取机制：从对话中识别关键信息并保存为记忆
  - 用户画像整合：每次对话时自动整合用户的作息、测评、打卡、记忆等信息
- **个性化对话**：AI 回复基于用户独特画像 + 专业知识
  - 系统提示词动态注入：用户画像 + 对话历史 + 专业知识
  - 记忆重要性评分（1-10）和访问次数追踪
- **新增文件**：
  - `backend/app/core/psychology_roles.py`：10 个专业 AI 角色配置
  - `backend/app/models/user_memory.py`：记忆和洞察数据模型
  - `backend/app/services/memory_service.py`：记忆管理服务
  - `backend/app/core/add_memory_tables.sql`：数据库迁移脚本
- **修改**：
  - `ai_service.py`：整合用户画像和专业知识到 AI 对话，添加自动洞察提取
  - `ai_role.py`：添加与知识库的多对多关系
  - `init_db.py`：加载 10 个新角色和专业知识
- **测试账号**：admin / admin123（已存在）

## 2025-09-18
- 初始化 Docker 化：新增 `docker-compose.yml`，编排 MySQL/Redis/Backend/Frontend/Seed。
- 新增后端 `Dockerfile`，使用 `uvicorn` 运行 FastAPI。
- 新增前端 `Dockerfile`，构建产物用 Nginx 托管并反代 `/api`。
- 新增 `frontend/nginx.conf` 代理 `/api` → `backend:8000`。
- 后端依赖增加：`python-multipart`（文件上传）、`PyMuPDF`（PDF 解析）。
- `app/core/init_db.py` 导入全部模型，改为仅创建不存在的表。
- 前端 `src/api/index.js` 支持 `VITE_API_BASE` 并默认走 `/api` 代理。

## 2025-09-23
- 前端：`aiApi.chat` 支持通过 `opts.extraFields` 传递可选字段（例如 `image_data_url`），避免页面层重写 body，兼容旧调用。
- 页面：`AiRoles.vue` 改为使用 `opts.extraFields.image_data_url` 传参。
- 文档：`PROJECT_STATUS.md` 更正上传说明：`/upload/image` 返回 `{url,data_url}`；`/upload/audio` 仅返回 `{url}`。
 - 后端：统一默认 `AI_API_URL=https://api.gpt.ge/v1/chat/completions`、`AI_MODEL=gpt-4o-mini`；新增 `AI_IMAGE_INPUT_MODE` 占位配置（默认 `data_url`，不改变现有行为）。
 - 后端：改进外部接口错误提示，对 413/422 提供更友好文案（尺寸/格式建议）。
 - 文档：在 `PROJECT_STATUS.md` 新增“附录一：前端按钮与后端接口映射”。
 - 前端：完善页面
   - `PlanProfile.vue`：新增作息表单（保存/生成/历史）。
   - `LiteratureList.vue`：新增上传、列表、分段与检索。
   - `RewardsPoints.vue`：新增积分总览与历史。
 - 前端：新增路由登录守卫（除 `/login`、`/register` 其余需登录）。
 - 配置：新增根目录 `.env` 示例并启用外部模型（`AI_USE_EXTERNAL=true`、`AI_API_URL`、`AI_API_KEY`、`AI_MODEL=gpt-4o-all`）。
