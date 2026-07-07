# 运维辅助系统 (Ops Assistant)

帮助运维团队快速定位和解决客户故障工单，同时沉淀处理经验为团队知识库。

## 快速启动

```bash
docker-compose up -d
```

启动后：
- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- 数据库: localhost:3306

默认管理员账号: admin / admin123

## 开发环境

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 技术栈

- 前端: React + TypeScript + Ant Design + Vite
- 后端: Python + FastAPI + SQLAlchemy + MySQL
- AI: LLM API (可配置)
