# Hai 后端服务

基于 FastAPI + MySQL + Redis

## 目录结构

```
backend/
├── app/
│   ├── main.py           # FastAPI 启动入口
│   ├── api/              # 路由/接口
│   ├── models/           # ORM模型
│   ├── schemas/          # Pydantic数据校验
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   └── core/             # 配置、数据库初始化
├── requirements.txt      # 依赖
└── README.md
```

## 启动方法

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 启动服务

```bash
uvicorn app.main:app --reload
```

3. 默认端口：8000

---

如需自定义数据库/Redis配置，请修改 `app/core/config.py`。 