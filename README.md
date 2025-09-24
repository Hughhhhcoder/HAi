# Hai 心理助手应用（FastAPI + Vue 3）

本项目提供一个围绕心理健康的全栈示例：用户登录、AI 对话、心理测评、每日打卡、积分与文献检索。已完整容器化，支持一键启动。

## 技术栈
- 后端：FastAPI、SQLAlchemy、MySQL、Redis
- 前端：Vue 3 + Vite + Tailwind CSS
- 构建与部署：Docker、docker-compose、Nginx（前端静态托管与 /api 反向代理）

## 目录结构
```
backend/           # FastAPI 源码与依赖
frontend/          # Vue 3 源码
uploads/           # 运行时上传目录（容器卷挂载）
docker-compose.yml # 编排 MySQL/Redis/Backend/Frontend/Seed
```

## 快速开始（Docker）
1) 准备环境变量（可选，默认值见 compose）
- 如需自定义，请创建 `.env` 并填入：
```
MYSQL_USER=hai
MYSQL_PASSWORD=hai123
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=aidb
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
VVEAI_API_URL=https://api.vveai.com/panel/token
VVEAI_API_KEY=change-me
```

2) 一键启动
```
docker compose up -d --build
```
- 前端：`http://localhost:5173`
- 后端：`http://localhost:8000`（也可通过前端 Nginx 代理 `http://localhost:5173/api` 访问）
- MySQL：本地 3306 暴露
- Redis：本地 6379 暴露

3) 初始化数据
- 编排中包含 `seed` 服务，会在后端启动后执行 `app.core.init_db`：
  - 确保所有模型表已创建
  - 插入默认 AI 角色
  - 创建测试账号：`admin / admin123`

## 开发说明
- 前端容器使用 Nginx 静态托管，`/api` 反代至 `backend:8000`
- 前端运行时 API 基地址：`/api`，可通过 `VITE_API_BASE` 覆盖（见 `src/api/index.js`）
- 后端上传目录 `/app/uploads` 已挂载命名卷 `backend_uploads`

## 常用命令
- 查看日志
```
docker compose logs -f backend
```
- 重新构建
```
docker compose build --no-cache && docker compose up -d
```
- 重跑初始化（按需）
```
docker compose run --rm seed
```
- 停止并清理
```
docker compose down
```

## 测试与自检
- 健康检查：`GET /ping` → `{ "msg": "pong" }`
- 登录：`POST /user/login`（使用 admin/admin123）
- AI 角色：`GET /ai/roles`
- 心理问卷：`GET /psych/questionnaire?test_type=PHQ9`
- 打卡：`POST /checkin/daily`

前端提供 `ApiTest` 页面便于快速验证。

## 生产注意事项
- 将数据库账号、密钥配置到外部安全存储，不使用默认值
- 配置持久化存储（当前已挂载 MySQL 与上传卷）
- 增加认证授权（JWT/Cookie），限制敏感接口
- 配置 HTTPS 与反向代理（生产 Nginx/Traefik）

## 变更日志
请见 `CHANGELOG.md`，记录了容器化改造及后续更新。
