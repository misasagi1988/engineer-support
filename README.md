# 运维辅助系统 (Ops Assistant)

帮助运维团队快速定位和解决客户故障工单，同时沉淀处理经验为团队知识库。

## 快速启动 (Docker)

```bash
docker-compose up -d
# 初始化数据库（首次启动）
docker-compose exec backend python init_db.py
```

启动后访问：
- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

默认管理员账号: **admin / admin123**

---

## 开发环境

### 前置条件
- Python 3.11+
- Node.js 18+
- MySQL 8.0（或使用 docker-compose 中的 MySQL）

### 1. 后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 或编辑现有 .env）
# 至少确保 SECRET_KEY 和 DATABASE_URL 已设置

# 初始化数据库表（首次运行）
python init_db.py

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后访问 http://localhost:8000/health 确认服务正常。

### 2. 前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端默认运行在 http://localhost:3001，会自动代理 `/api` 请求到后端 `localhost:8000`。

---

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── api/           # 路由层
│   │   ├── models/        # SQLAlchemy ORM 模型
│   │   ├── schemas/       # Pydantic 请求/响应模型
│   │   ├── services/      # 业务逻辑层
│   │   ├── db/            # 数据库连接与会话管理
│   │   ├── config.py      # 配置管理
│   │   └── main.py        # FastAPI 入口
│   ├── .env               # 环境变量
│   ├── init_db.py         # 数据库初始化脚本
│   └── requirements.txt   # Python 依赖
├── frontend/
│   ├── src/
│   │   ├── api/           # API 请求封装
│   │   ├── pages/         # 页面组件
│   │   ├── components/    # 公共组件
│   │   ├── store/         # 状态管理 (Zustand)
│   │   └── types/         # TypeScript 类型定义
│   ├── vite.config.ts     # Vite 配置
│   └── package.json
└── docker-compose.yml
```

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | React + TypeScript + Ant Design + Vite |
| 后端 | Python + FastAPI + SQLAlchemy (async) |
| 数据库 | MySQL 8.0+ |
| AI | LLM API (可配置，支持切换不同模型) |
| 部署 | Docker Compose |
