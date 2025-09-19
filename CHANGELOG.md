# 更新日志

## 2025-09-18
- 初始化 Docker 化：新增 `docker-compose.yml`，编排 MySQL/Redis/Backend/Frontend/Seed。
- 新增后端 `Dockerfile`，使用 `uvicorn` 运行 FastAPI。
- 新增前端 `Dockerfile`，构建产物用 Nginx 托管并反代 `/api`。
- 新增 `frontend/nginx.conf` 代理 `/api` → `backend:8000`。
- 后端依赖增加：`python-multipart`（文件上传）、`PyMuPDF`（PDF 解析）。
- `app/core/init_db.py` 导入全部模型，改为仅创建不存在的表。
- 前端 `src/api/index.js` 支持 `VITE_API_BASE` 并默认走 `/api` 代理。
