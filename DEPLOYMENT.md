# 运维辅助系统 — 本地运行指南

## 环境要求

| 组件 | 最低版本 |
|------|----------|
| Python | 3.12+ |
| Node.js | 18+ |
| MySQL | 8.0+ |

## 一、数据库准备

### 1.1 确认 MySQL 可访问

确保目标机器能访问 MySQL 服务器（`10.43.102.51:3399`），且数据库 `engineer_support` 已创建。

### 1.2 授权数据库用户

在 MySQL 服务器上执行：

```sql
-- 允许 root 从任意 IP 连接（生产环境建议限制 IP 范围）
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'S3cur!ty@qihoo.com';
GRANT ALL PRIVILEGES ON engineer_support.* TO 'root'@'%';
FLUSH PRIVILEGES;
```

> 如果同事的机器 IP 无法被数据库白名单放行，需要联系 DBA 为其 IP 授权，或改用一台数据库可访问的服务器统一部署。

## 二、后端部署

### 2.1 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2.2 配置环境变量

编辑 `backend/.env`，确认以下配置正确：

```
LLM_API_KEY=
LLM_API_BASE=
LLM_MODEL=gpt-4o-mini
SECRET_KEY=dev-secret-key
DATABASE_URL=mysql+aiomysql://root:S3cur%21ty%40qihoo.com@10.43.102.51:3399/engineer_support
```

> **注意**：`DATABASE_URL` 中的密码包含特殊字符 `!@`，已做 URL 编码（`%21` = `!`，`%40` = `@`），修改密码时需重新编码。

### 2.3 初始化数据库

```bash
cd backend
python init_db.py
```

此步骤会：
- 创建所有数据表
- 插入默认管理员账号（用户名 `admin`，密码 `admin123`）

### 2.4 启动后端服务

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

> `--host 0.0.0.0` 让服务监听所有网卡，支持局域网访问。生产部署建议用 `--host 127.0.0.1` + Nginx 反向代理。

验证：访问 `http://localhost:8000/health`，返回 `{"status": "ok"}` 即正常。

## 三、前端部署

### 3.1 安装依赖

```bash
cd frontend
npm install
```

### 3.2 启动开发服务器

```bash
cd frontend
npm run dev
```

默认监听 `http://localhost:3001`，Vite 配置已包含：
- `host: '0.0.0.0'` — 支持局域网访问
- `allowedHosts: true` — 允许任意 Host 请求
- `/api` 代理到 `http://localhost:8000`

访问 `http://localhost:3001/login` 即可看到登录页。

## 四、局域网访问配置

### 4.1 后端 CORS

后端 CORS 已配置为允许所有来源（`allow_origins=["*"]`），开发阶段无需额外修改。

### 4.2 获取本机 IP

```bash
ipconfig
```

找到局域网 IP（通常是 `10.x.x.x` 或 `192.168.x.x`），同事通过 `http://你的IP:3001/login` 访问。

### 4.3 防火墙放行（如被拦截）

如果同事 ping 得通但访问不了，可能是 Windows 防火墙拦截了端口：

```bash
netsh advfirewall firewall add rule name="Vite 3001" dir=in action=allow protocol=TCP localport=3001
netsh advfirewall firewall add rule name="Uvicorn 8000" dir=in action=allow protocol=TCP localport=8000
```

如果 ping 都不通，检查 Windows 网络类型是否为"专用网络"（公用网络默认阻止入站），或联系 IT 开通端口权限。

## 五、生产部署建议

开发服务器不适合生产使用。正式部署建议：

1. **前端构建**：`npm run build` → 生成静态文件 → 用 Nginx 托管
2. **后端部署**：用 Gunicorn + Uvicorn workers 替代开发模式
3. **反向代理**：Nginx 统一代理前端静态文件和后端 API
4. **容器化**：项目已有 `docker-compose` 配置，可直接 `docker compose up -d` 一键启动

## 六、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 登录后页面闪一下又回到登录页 | 数据库未初始化 / 无 admin 用户 | 运行 `python init_db.py` |
| 500 Internal Server Error | 数据库连接失败 / 密码错误 | 检查 `.env` 中 DATABASE_URL 是否正确 |
| /api/auth/me 返回 401 | CORS 未放行 / token 未正确保存 | 确认后端 allow_origins 包含前端地址 |
| bcrypt 版本报错 | passlib 与 bcrypt 4.x 不兼容 | 已修复，改用原生 bcrypt 库 |
