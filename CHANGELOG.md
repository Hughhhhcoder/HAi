# 更新日志

## 2025-10-14
- **AI 角色升级**：从 2 个通用角色扩展为 10 个专业心理健康 AI 角色
  - 新增专业角色：温暖倾听者·艾米、认知教练·理查德、正念导师·静心、积极心理师·阳光、情绪专家·心涟、创伤疗愈师·守护、青少年导师·星辰、职场心理顾问·行远、关系咨询师·和鸣、生命意义探索者·启明
  - 每个角色基于真实心理学流派（人本主义、CBT、正念、积极心理学、EFT 等）
  - 角色提示词包含专业背景、咨询风格、核心方法和咨询原则
- **长期记忆系统**：AI 可以逐渐了解用户
  - 新增 `user_memories` 表：存储用户性格、困扰、目标、触发因素等记忆
  - 新增 `user_insights` 表：存储用户深层洞察（核心特质、应对模式等）
  - 自动提取机制：从对话中识别关键信息并保存为记忆
  - 用户画像整合：每次对话时自动整合用户的作息、测评、打卡、记忆等信息
- **个性化对话**：AI 回复基于用户独特画像
  - 系统提示词动态注入用户画像和对话历史
  - 记忆重要性评分（1-10）和访问次数追踪
- **后端新增文件**：
  - `backend/app/core/psychology_roles.py`：10 个专业 AI 角色配置
  - `backend/app/models/user_memory.py`：记忆和洞察数据模型
  - `backend/app/services/memory_service.py`：记忆管理服务
  - `backend/app/core/add_memory_tables.sql`：数据库迁移脚本
- **后端修改**：
  - `ai_service.py`：整合用户画像到 AI 对话，添加自动洞察提取
  - `init_db.py`：加载 10 个新角色替代原有 2 个角色
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
