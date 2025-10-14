项目现况（截至：2025-10-14）

一、总体概览
- 前端：Vue 3 + Composition API，Vite，Tailwind CSS，Nginx 容器静态托管，开发/生产通过前端容器反代后端（/api、/static）。
- 后端：FastAPI，SQLAlchemy（MySQL），Redis（对话上下文），Uvicorn。已完成 Docker 化（docker-compose）。
- 数据库：MySQL（用户、AI 角色、对话、心理测评、打卡、积分、文献元数据与分段、**用户记忆与洞察**等表）。
- 部署：docker-compose 一键启动（mysql、redis、backend、frontend、seed），uploads 通过卷持久化，前端端口 5174（避免与其他项目冲突），后端端口 8000。
- 主要功能：
  - 用户注册/登录（bcrypt 哈希；当前为简化 Demo，未发放 JWT）。
  - **10 个专业心理健康 AI 角色**（人本主义、CBT、正念、积极心理学、EFT、创伤疗愈、青少年、职场、关系、存在主义）。
  - **长期记忆系统**：AI 自动记住用户性格、困扰、目标等，对话越多越了解用户。
  - **个性化对话**：每次回复基于用户画像（作息、测评、打卡、记忆）。
  - AI 对话（角色选择、历史记录、清空会话），支持图片上传（最大 50MB）与消息内预览。
  - 心理测评（PHQ9、GAD7）、生活作息信息、恢复计划生成（mock）、每日打卡与积分。
  - 文献上传（PDF/TXT）、自动分段与检索（关键词计数 mock）。

二、目录与服务简述
- backend/app/api
  - user：/user/register、/user/login
  - ai：/ai/roles（返回 10 个专业心理角色）、/ai/chat、/ai/history、/ai/clear、/ai/stream（SSE）。
  - upload：/upload/image 返回 {url, data_url}；/upload/audio 返回 {url}（无 data_url）。
  - literature：上传/列表/分段/检索。
  - psych、plan、checkin、rewards：心理测评、作息与计划、每日打卡、积分查询。
- backend/app/services
  - user_service：注册/验证（bcrypt）。
  - **memory_service（新增）**：
    - 用户画像生成：整合作息、测评、打卡、记忆等多维度信息。
    - 记忆管理：添加/查询用户记忆（personality, concern, goal, trigger 等类型）。
    - 洞察提取：从对话中自动识别关键信息并保存。
  - ai_service：
    - 对话保存/查询、Redis 上下文（chatctx:{user}:{role}）。
    - **用户画像整合**：每次对话自动注入用户画像到 AI 提示词。
    - **自动记忆提取**：对话后自动提取洞察更新用户记忆。
    - 外部大模型调用（OpenAI 风格），消息体支持 {type:text}/{type:image_url}；失败自动降级为文本包含图片链接。
    - SSE 流式生成器（call_external_chat_api_stream，前端支持但默认已回退到一次性渲染）。
- backend/app/core
  - **psychology_roles.py（新增）**：10 个专业心理 AI 角色配置，包含角色名、专业背景、咨询风格、核心方法、提示词模板。
  - init_db.py：初始化数据库表和加载 10 个专业角色。
- backend/app/models
  - **user_memory.py（新增）**：UserMemory（用户记忆）、UserInsight（用户洞察）数据模型。
- frontend
  - 统一 API 封装（/src/api/index.js），开发态走 /api 代理；容器生产由 Nginx 反代 /api、/static。
  - `aiApi.chat` 支持通过 `opts.extraFields` 传入 `image_data_url` 等扩展字段，避免页面层重写 body。
  - 布局：MainLayout（Header+Sidebar+Content，移动端抽屉），响应式。
  - 页面：登录/注册/Home/AI 对话/心理测评/计划/打卡/积分/文献。

三、环境与运行
- docker-compose.yml（关键环境变量）：
  - MySQL/Redis：连接参数。
  - AI 调用：
    - AI_USE_EXTERNAL=true（启用外部 AI）
    - AI_API_URL=https://api.gpt.ge/v1/chat/completions
    - AI_API_KEY（已配置）
    - AI_MODEL=gpt-4o-all（支持多模态）
    - AI_TEMPERATURE / AI_TOP_P / AI_MAX_TOKENS
    - AI_IMAGE_INPUT_MODE=data_url（图片以 base64 传递，不依赖外部 URL）
    - PUBLIC_BASE_URL（可选，用于 https 模式的图片 URL 拼接）
- 前端 Nginx：
  - /api → backend:8000（HTTP/1.1，buffering off，用于 SSE）。
  - /static → backend:8000（代理后端静态文件）。
  - /uploads → 直接暴露容器内挂载的上传目录（避免跨隧道回源失败）。
  - client_max_body_size 50M（支持大图片上传）。
- 访问地址：
  - 前端：http://localhost:5174
  - 后端：http://localhost:8000
  - 接口文档：http://localhost:8000/docs

四、近期变更（关键里程碑）
1) **AI 心理健康专业化升级（2025-10-14）**
   - 10 个专业心理 AI 角色替代原有 2 个通用角色
   - 长期记忆系统：AI 会记住用户性格、困扰、目标等
   - 个性化对话：基于用户画像（作息、测评、打卡、记忆）生成回复
   - 自动洞察提取：从对话中识别关键信息并保存
   - 数据库新增 user_memories 和 user_insights 表
   - 新增 memory_service 服务和 psychology_roles 配置
2) 容器化与文档
   - 新增 backend/frontend Dockerfile；docker-compose 一键启动；README 与 CHANGELOG 整理。
3) 前后端联调与对话体验
   - 修复 AI 回复字段不一致（前端读取 reply；后端返回 reply）。
   - 新增 /ai/clear 清空历史（数据库+Redis）。
   - 修复图片上传后不立即显示在聊天框的问题。
   - Markdown 渲染 + DOMPurify 清洗（AI 回复排版更清晰）。
4) 图片上传与多模态
   - /upload/image 返回 {url, data_url}；前端发送时携带 image_url 与 image_data_url。
   - Nginx client_max_body_size 提升至 50M 支持大图片。
   - AI_IMAGE_INPUT_MODE=data_url（图片以 base64 传递，稳定可靠）。
   - 外部模型调用：OpenAI 风格 messages.content = [{type:text},{type:image_url:{url}}]。
   - 若上游 400/404，自动降级为把图片 URL 拼进文本后重试。
5) AI 模型与平台
   - 当前使用：api.gpt.ge + gpt-4o-all（支持多模态）
   - 图片传递：data_url 模式（不依赖外部 URL，更稳定）

五、当前功能状态
- 注册/登录：
  - 前端注册与后端接口已打通；curl 测试可登录；无 JWT，Demo 级别。
  - 测试账号：admin / admin123
- **AI 对话（已升级）**：
  - **10 个专业心理角色**：温暖倾听者、认知教练、正念导师、积极心理师、情绪专家、创伤疗愈师、青少年导师、职场心理顾问、关系咨询师、生命意义探索者。
  - **长期记忆**：AI 自动记住用户提到的性格、困扰、目标、触发因素等。
  - **个性化回复**：每次对话基于用户画像（作息、测评、打卡、记忆）。
  - 角色加载、历史读取、清空历史正常。
  - 发送文本：正常，Markdown 渲染可读。
  - 发送图片：
    - 上传与预览：成功（最大 50MB，立即显示在聊天框）。
    - 模型理解：gpt-4o-all 正常识别图片并回复（data_url 模式）。
- 心理测评：PHQ9、GAD7 问卷提交和历史查询正常。
- 打卡与积分：每日打卡+5分，积分历史可查。
- 文献上传：PDF/TXT 解析和分段检索（mock）正常。
- 静态资源：
  - 前端 5174/static/* 和 /uploads/* 可访问。

六、已知问题与待优化项
1) **长期记忆提取精度（待优化）**
   - 当前使用简单关键词匹配提取洞察，准确性有限。
   - 未来可改用：
     - 调用 AI 从对话中提取结构化洞察（更准确）
     - NLP 技术（情感分析、实体识别）
     - 用户确认机制（AI 询问"我理解对了吗？"）

2) 认证与安全（非阻塞）
   - 登录未发 token（JWT/Cookie），仅 Demo；后续对敏感接口需鉴权与角色权限控制。

3) 前端用户体验优化
   - 用户可查看自己的记忆和画像（"我的画像"页面）
   - 每个 AI 角色的专业介绍和适合问题展示
   - 记忆管理（用户可编辑/删除不准确的记忆）

七、风险与影响
- 外部 API 依赖：模型名/计费/限流/网络情况会直接影响用户体验。
- 图片敏感数据：data:URL 会增大请求体，需关注日志与隐私合规；生产建议改为 https 私有对象存储（临时签名 URL）。
- 安全：未鉴权的接口在生产环境不可用；需尽快加 JWT 与 CSRF/速率限制。
- **用户隐私**：长期记忆存储用户敏感信息（性格、困扰等），需确保数据安全和隐私合规。
- **伦理责任**：AI 仅供心理健康支持，不能替代专业心理治疗；需在前端添加免责声明。

八、验证与排错清单（可即刻使用）
1) 健康检查
```
curl -s http://localhost:8000/ping
```
2) 图片直连（经前端反代）
```
curl -I http://localhost:5173/static/images/<文件名>.png
```
3) 上传图片（返回 url 与 data_url）
```
curl -s -X POST http://localhost:5173/api/upload/image \
  -F file=@/path/to/image.jpg | jq
```
4) 文字消息
```
curl -s -X POST http://localhost:5173/api/ai/chat \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'user_id=1&role_id=1&message=你好' | jq
```
5) 图片+文字（多模态）
```
# 先上传得到 data_url
# 再提交 /ai/chat，传 image_data_url=data:image/jpeg;base64,...
# 示例：
curl -s -X POST http://localhost:5173/api/ai/chat \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "user_id=1&role_id=1&message=看下这张图&image_data_url=$(cat /path/to/image.b64.txt)" | jq
```

6) 体积/格式错误友好提示
```
# 当上游返回 413/422 时，后端会提示：
# "请求体过大或格式不被支持。若包含图片，请尝试降低分辨率/文件大小，或改用 https 公网 URL。"
```

九、下一步计划（优先级从高到低）
P0 **长期记忆系统优化**
- AI 自动生成用户洞察摘要（调用 AI 总结对话）
- 记忆重要性自动衰减（长时间未提及的记忆降低权重）
- 前端"我的画像"页面，展示 AI 对用户的理解
- 用户可编辑/删除/确认记忆

P1 **前端角色展示优化**
- 每个 AI 角色的专业介绍、适合问题、咨询风格展示
- 角色选择时显示角色头像/图标
- 添加免责声明（AI 不能替代专业心理治疗）

P2 认证与安全
- 登录改 JWT（/login 返回 access/refresh token），前端持久化；后端在需要处校验。
- CORS、速率限制、请求体大小限制；敏感操作审计日志。
- 用户数据加密存储（特别是记忆和洞察）

P3 对话体验增强
- 前端添加"失败重试"、"停止生成" 与"复制回复"按钮。
- 历史会话列表、会话重命名/删除。
- 图片/音频预览样式优化，进度与错误状态可视化。
- AI 主动关怀（"我注意到你最近提到..."）

P4 文献与检索
- 引入真实向量索引（FAISS/pgvector），语义检索与引用片段高亮。

十、变更记录（摘要）
- **2025-10-14 重大升级**：
  - 10 个专业心理 AI 角色（基于真实心理学流派）
  - 长期记忆系统（user_memories、user_insights 表）
  - 个性化对话（用户画像自动整合）
  - 图片上传立即显示修复
  - Nginx client_max_body_size 50M
  - 前端端口改为 5174
- 新增：Docker 化、Nginx 反代配置、/ai/clear、/ai/stream、Markdown 渲染、图片上传与预览、memory_service。
- 修复：前端与后端字段不一致、/static 反代 404、CORS 设置、SSE 反代参数、图片上传后聊天框不显示。
- 调整：
  - AI_API_URL：api.gpt.ge
  - AI_MODEL：gpt-4o-all（支持多模态）
  - AI_IMAGE_INPUT_MODE：data_url（稳定可靠）

十一、结论
- **Hai 已从通用 AI 聊天应用升级为专业心理健康支持平台**。
- 10 个专业 AI 角色覆盖多种心理问题和咨询需求。
- 长期记忆系统让 AI 会越来越了解用户，提供个性化支持。
- 系统架构稳定，前后端交互畅通，图片上传与多模态对话已闭环。
- 后续重点：优化记忆提取精度、前端用户体验、安全与隐私保护。


附录一：前端按钮与后端接口映射
- 登录页
  - 按钮：Sign in → 接口：`POST /user/login`
- 首页模块
  - 立即打卡 → 路由 `/checkin/daily`
  - 开始测评 → 路由 `/psych/choose`
  - 开始对话 → 路由 `/ai/roles`
  - 康复计划 → 路由 `/plan/profile`
  - 文献资料 → 路由 `/literature/list`
  - 积分奖励 → 路由 `/rewards/points`
  - 退出登录 → 本地清理存储 + 路由 `/login`
- AI 对话页（`AiRoles.vue`）
  - 选择角色卡片 → `GET /ai/roles`（进入会话后使用 `GET /ai/history`）
  - 返回 ← → 返回角色列表（前端状态）
  - 清空聊天 → `POST /ai/clear`
  - 图片 → `POST /upload/image`（返回 `{url,data_url}`）
  - 发送 → `POST /ai/chat`（可含 `image_data_url`）
- 心理测评页（`PsychChoose.vue`）
  - 开始 PHQ9/GAD7 → `GET /psych/questionnaire?test_type=...`
  - 上一题/下一题/完成测评 → `POST /psych/submit?user_id=...&test_type=...`（JSON 数组 body）
  - 重新测评/取消 → 前端状态
- 每日打卡页（`CheckinDaily.vue`）
  - 情绪选择 → 前端状态
  - 完成打卡 → `POST /checkin/daily?user_id=...&mood=...&sleep_hours=...&completed_tasks=...`
  - 查看更多记录 → 预留（控制台日志）
- 文献页
  - 上传 → `POST /literature/upload`
  - 列表/分段/检索 → `GET /literature/list|/chunks|/search`
- 积分页
  - 查看积分 → `GET /rewards/points`
  - 历史 → `GET /rewards/history`
