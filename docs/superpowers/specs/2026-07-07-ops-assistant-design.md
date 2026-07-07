# 运维辅助系统设计文档

**日期**: 2026-07-07
**状态**: 待审核
**作者**: Claude Code

---

## 1. 背景与目标

### 1.1 问题背景

- 运维团队 3-5 人，日均承接 30+ 客户问题单
- 产品已迭代多版本，多模块，不同模块有不同问题类型
- 产品在客户端**私有化部署**，部署模式分为：单机、HA、集群、上下级
- 不同部署模式下，同一问题的排查路径和根因可能不同
- 问题承接渠道混合（工单系统、即时通讯等）
- 运维处理时需留存客户日志、配置、报错截图等附件
- 运维经验散落在个人手中，难以复用和传承

### 1.2 系统目标

本产品的两大核心目标：

1. **辅助运维快速定位、解决客户故障工单** — 智能识别问题归属（模块/版本/部署模式），推荐相似案例和排查路径，缩短故障处理时间
2. **沉淀运维故障处理经验，形成团队知识库** — 处理过程半自动归档为案例，持续积累可检索、可复用的知识资产

支撑能力：
- 附件管理（日志/配置/截图留存）
- 客户与部署实例管理
- 统计与报表

### 1.3 用户角色

| 角色 | 权限 |
|------|------|
| 管理员 | 系统配置、模块/版本管理、排查路径管理、知识库审核 |
| 运维人员 | 处理工单、使用智能定位、查阅知识库、创建和确认案例 |

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        浏览器 (React SPA)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ 工单管理  │ │ 智能定位  │ │ 知识库   │ │ 管理后台     │    │
│  │          │ │ ◄目标1   │ │ ◄目标2   │ │              │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI 后端                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ 工单服务  │ │ 推荐引擎  │ │ 知识服务  │ │ 用户服务     │    │
│  │ ◄目标1   │ │ ◄目标1+2 │ │ ◄目标2   │ │              │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LLM Client (AI 能力)                     │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    MySQL                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ tickets  │ │ cases    │ │ customers│ │ users        │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 技术栈

| 层 | 技术 | 说明 |
|---|------|------|
| 前端 | React + TypeScript + Ant Design + Vite | 企业级组件，开发效率高 |
| 后端 | Python + FastAPI + SQLAlchemy + Pydantic | 异步高性能，类型安全 |
| 数据库 | MySQL 8.0+ | FULLTEXT 全文检索 + JSON 类型 |
| AI | LLM API | 可配置，支持切换不同模型 |
| 部署 | Docker Compose | 开发/生产环境一致 |

---

## 3. 核心功能

### 3.1 智能定位

**流程**: 问题描述 → 模块识别 → 版本识别 → 根因匹配 → 方案推荐 → 运维确认

1. **模块自动识别** — LLM 分析 + 关键词匹配，预判问题归属模块，运维可修改确认
2. **版本自动识别** — 从问题描述/报错中提取版本号，支持模糊匹配
3. **根因快速匹配** — 基于历史案例特征库（错误码、关键词、现象描述），匹配相似根因
4. **解决方案推荐** — 按模块维度检索历史解决方案，按相似度排序推荐 Top 3
5. **排查路径推荐** — 按模块提供标准化排查步骤清单（checklist），运维可勾选已完成步骤

### 3.2 工单管理

- **工单 CRUD** — 创建、查看、编辑、关闭工单
- **多渠道接入** — adapter 模式对接 Jira/企微/手动录入。MVP 阶段以手动录入和复制粘贴为主，V2 实现 Jira API 对接
- **状态流转** — 待处理 → 处理中 → 已解决 → 已关闭
- **优先级管理** — P0/P1/P2/P3 四级
- **自动关联** — 处理完成后自动关联对应案例

### 3.3 经验沉淀

**流程**: 处理工单 → 填写解决方案 → 点击"生成案例" → AI 自动整理 → 人工确认 → 入库

1. **半自动记录** — 处理过程中系统提示记录关键步骤
2. **一键生成** — 处理完成后，AI 自动整理为案例草稿
3. **人工确认** — 运维审核确认后案例入库
4. **标签与检索** — 案例支持标签分类、全文搜索、按模块筛选

### 3.4 知识库

- **案例浏览** — 按模块、标签、时间浏览案例
- **全文搜索** — PostgreSQL 全文检索
- **案例详情** — 根因分析、解决方案、排查路径、关联工单
- **案例复用** — 新工单自动推荐相似案例

### 3.5 运维工作台

- **待办列表** — 按优先级展示我的待办工单
- **推荐案例** — 基于当前待办推荐高匹配度案例
- **快捷入口** — 新建工单、智能定位、知识库一键跳转
- **统计概览** — 今日处理量、解决率、模块分布

### 3.6 管理后台

- **客户管理** — 客户信息维护、合同等级、联系方式
- **部署实例管理** — 客户的部署实例登记（名称、部署模式、版本、环境、配置摘要）
- **模块管理** — 产品模块的增删改查
- **版本管理** — 产品版本的增删改查
- **排查路径管理** — 按模块和部署模式配置排查步骤模板
- **用户管理** — 角色分配、权限管理
- **案例审核** — 审核运维提交的案例草稿
- **附件管理** — 附件存储统计、清理策略配置

---

## 4. 数据模型

### 4.1 MySQL 类型映射

数据模型表中使用逻辑类型，SQLAlchemy ORM 自动映射为 MySQL 类型：

| 逻辑类型 | MySQL 实际类型 | 说明 |
|---------|---------------|------|
| UUID | CHAR(36) | 存储 UUID 字符串 |
| jsonb | JSON | MySQL 5.7+ JSON 类型 |
| text[] | JSON | MySQL 无原生数组，用 JSON 数组存储 |
| enum | ENUM | MySQL 原生 ENUM |
| datetime | DATETIME | MySQL DATETIME |

---

### 4.2 用户与角色

**users**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 用户 ID |
| username | string (50) | 用户名 |
| email | string (100) | 邮箱 |
| password_hash | string (255) | 密码哈希 |
| role | enum (admin/operator) | 角色 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.3 客户与部署

**customers**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 客户 ID |
| name | string (200) | 客户名称 |
| contract_level | enum (vip/standard/basic) | 合同等级 |
| contact_info | text | 联系方式 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

**deployments**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 部署实例 ID |
| customer_id | UUID (FK → customers) | 所属客户 |
| name | string (200) | 部署名称（如"客户A-生产环境"） |
| deploy_mode | enum (standalone/ha/cluster/hierarchical) | 部署模式：单机/HA/集群/上下级 |
| version_id | UUID (FK → versions) | 当前产品版本 |
| environment | enum (production/staging/test) | 环境类型 |
| config_summary | JSON | 关键配置摘要（CPU/内存/存储/网络等） |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.4 附件

**attachments**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 附件 ID |
| ticket_id | UUID (FK → tickets) | 关联工单 |
| case_id | UUID (FK → cases, nullable) | 关联案例（可为空，案例沉淀时关联） |
| file_name | string (500) | 原始文件名 |
| file_type | enum (log/config/screenshot/other) | 附件类型 |
| file_size | bigint | 文件大小（字节） |
| storage_path | string (1000) | 存储路径（S3/本地文件系统） |
| description | text | 附件描述 |
| uploaded_by | UUID (FK → users) | 上传人 |
| created_at | datetime | 上传时间 |

### 4.5 产品配置

**modules**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 模块 ID |
| name | string (100) | 模块名称 |
| description | text | 模块描述 |
| created_at | datetime | 创建时间 |

**versions**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 版本 ID |
| name | string (50) | 版本号 |
| release_date | date | 发布日期 |
| is_active | boolean | 是否活跃 |
| created_at | datetime | 创建时间 |

**troubleshooting_paths**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 路径 ID |
| module_id | UUID (FK → modules) | 所属模块 |
| deploy_mode | enum (all/standalone/ha/cluster/hierarchical) | 适用部署模式，all 表示通用 |
| steps | JSON | 排查步骤列表 `[{id, title, description, order}]` |
| version | string (20) | 路径模板版本 |
| created_by | UUID (FK → users) | 创建人 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.6 工单

**tickets**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 工单 ID |
| external_id | string (100) | 外部系统工单号（Jira 等） |
| customer_id | UUID (FK → customers) | 所属客户 |
| deployment_id | UUID (FK → deployments) | 所属部署实例 |
| title | string (200) | 问题标题 |
| description | text | 问题描述 |
| module_id | UUID (FK → modules) | 所属模块 |
| version_id | UUID (FK → versions) | 所属版本（从 deployment 自动带出） |
| deploy_mode | enum (standalone/ha/cluster/hierarchical) | 部署模式（从 deployment 自动带出） |
| source | enum (jira/wechat/manual) | 来源渠道 |
| status | enum (pending/processing/resolved/closed) | 状态 |
| priority | enum (p0/p1/p2/p3) | 优先级 |
| assignee_id | UUID (FK → users) | 处理人 |
| identified_root_cause | text | AI 识别的根因 |
| solution | text | 解决方案 |
| troubleshooting_checklist | JSON | 实际执行的排查步骤 `[{step_id, completed}]` |
| auto_identified | boolean | 模块/版本是否自动识别 |
| created_at | datetime | 创建时间 |
| resolved_at | datetime | 解决时间 |
| updated_at | datetime | 更新时间 |

### 4.7 案例与知识

**cases**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID (PK) | 案例 ID |
| ticket_id | UUID (FK → tickets) | 来源工单 |
| customer_id | UUID (FK → customers, nullable) | 来源客户（可为空，脱敏案例不关联） |
| title | string (200) | 案例标题 |
| module_id | UUID (FK → modules) | 所属模块 |
| deploy_mode | enum (standalone/ha/cluster/hierarchical) | 部署模式（不同模式根因可能不同） |
| root_cause | text | 根因分析 |
| solution | text | 解决方案 |
| troubleshooting_path | JSON | 排查路径模板 `[{step, description, result}]` |
| tags | JSON | 标签数组 `["tag1", "tag2"]` |
| confidence_score | float | 方案置信度（0-1） |
| review_status | enum (draft/reviewed/archived) | 审核状态 |
| reviewed_by | UUID (FK → users) | 审核人 |
| created_by | UUID (FK → users) | 创建人 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 4.8 ER 关系图

```
customers 1──N deployments
customers 1──N tickets
customers 1──N cases (nullable, for desensitized cases)

deployments 1──N tickets
deployments 1──N attachments

users 1──N tickets (assignee)
users 1──N cases (created_by)
users 1──N cases (reviewed_by)
users 1──N troubleshooting_paths (created_by)

modules 1──N tickets
modules 1──N cases
modules 1──N troubleshooting_paths

versions 1──N tickets
versions 1──N deployments

tickets 1──1 cases
tickets 1──N attachments

cases 1──N attachments
```

### 4.9 附件存储策略

- **存储方式**: 开发环境使用本地文件系统（`./storage/attachments/`），生产环境使用对象存储（S3/MinIO/OSS）
- **文件类型**: 日志（.log/.txt/.gz）、配置（.yaml/.json/.conf/.xml）、截图（.png/.jpg）、其他
- **大小限制**: 单文件最大 50MB，单工单附件总大小最大 500MB
- **命名规则**: `{ticket_id}/{timestamp}_{original_filename}`，按工单目录隔离
- **下载权限**: 仅工单处理人和管理员可下载附件

---

## 5. API 设计

### 5.1 认证

- **认证方式**: JWT（JSON Web Token），登录成功后返回 access token，后续请求在 Authorization header 中携带 `Bearer <token>`
- **Token 有效期**: access_token 24 小时，后续可加 refresh_token
- **密码加密**: bcrypt，salt rounds = 12

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 用户登录，返回 JWT |
| POST | `/api/auth/logout` | 用户登出（前端清除 token） |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 5.2 工单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tickets` | 工单列表（支持分页、筛选） |
| POST | `/api/tickets` | 创建工单 |
| GET | `/api/tickets/{id}` | 工单详情 |
| PUT | `/api/tickets/{id}` | 更新工单 |
| PUT | `/api/tickets/{id}/status` | 更新工单状态 |
| POST | `/api/tickets/{id}/generate-case` | 基于工单生成案例草稿 |

### 5.3 智能定位

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/ai/locate` | 智能定位（输入问题描述，返回模块/版本/部署模式/根因/方案推荐） |
| GET | `/api/ai/troubleshooting-path/{module_id}` | 获取模块排查路径（可选传 deploy_mode 过滤） |

### 5.4 附件

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tickets/{id}/attachments` | 上传附件（支持批量上传） |
| GET | `/api/tickets/{id}/attachments` | 获取工单附件列表 |
| GET | `/api/attachments/{id}` | 下载附件 |
| DELETE | `/api/attachments/{id}` | 删除附件 |

### 5.5 案例与知识

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cases` | 案例列表（支持分页、筛选、搜索） |
| POST | `/api/cases` | 创建案例 |
| GET | `/api/cases/{id}` | 案例详情 |
| PUT | `/api/cases/{id}` | 更新案例 |
| PUT | `/api/cases/{id}/review` | 审核案例 |
| POST | `/api/cases/search` | 全文搜索案例 |

### 5.6 管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/customers` | 客户列表 |
| POST | `/api/customers` | 创建客户 |
| GET | `/api/customers/{id}` | 客户详情（含部署实例） |
| PUT | `/api/customers/{id}` | 更新客户 |
| GET | `/api/deployments` | 部署实例列表（支持按客户筛选） |
| POST | `/api/deployments` | 创建部署实例 |
| PUT | `/api/deployments/{id}` | 更新部署实例 |
| GET | `/api/modules` | 模块列表 |
| POST | `/api/modules` | 创建模块 |
| PUT | `/api/modules/{id}` | 更新模块 |
| GET | `/api/versions` | 版本列表 |
| POST | `/api/versions` | 创建版本 |
| GET | `/api/troubleshooting-paths` | 排查路径列表 |
| POST | `/api/troubleshooting-paths` | 创建排查路径 |
| PUT | `/api/troubleshooting-paths/{id}` | 更新排查路径 |
| GET | `/api/users` | 用户列表（admin） |
| PUT | `/api/users/{id}/role` | 修改用户角色（admin） |

### 5.7 统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats/dashboard` | 工作台统计数据 |

---

## 6. 智能定位详细流程

```
1. 用户输入问题描述（或关联工单号/选择客户和部署实例）
2. 后端调用 LLM 分析（单次调用，结构化 prompt）：
   a. 提取可能的模块 → 返回 module_candidates
   b. 提取版本号 → 返回 version_candidates
   c. 分析部署模式特征 → 返回 deploy_mode_hints
   d. 分析根因关键词 → 返回 root_cause_candidates
   Prompt 格式：系统 prompt 中注入模块列表、版本列表、部署模式列表，要求 LLM 以 JSON 格式返回识别结果
3. 基于模块、部署模式和关键词，在 cases 表中检索相似案例：
   a. MySQL FULLTEXT 全文检索
   b. 按模块 + 部署模式 + 置信度综合排序，取 Top 5
4. 加载该模块 + 部署模式的排查路径模板（优先加载匹配部署模式的路径，回退到通用路径）
5. 返回前端：
   - module_candidates（含置信度）
   - version_candidates（含置信度）
   - deploy_mode_hints
   - root_cause_candidates
   - similar_cases（含相似度评分、部署模式标签）
   - troubleshooting_path（步骤列表）
6. 运维确认模块/版本/部署模式 → 开始按排查路径处理
```

### 降级策略

- **LLM 不可用** → 降级为关键词匹配（错误码 + 模块关键词），功能可用但准确度降低
- **无相似案例** → 返回空推荐列表，提示手动检索知识库
- **模块识别失败** → 列出全部模块供手动选择

---

## 7. 错误处理

| 场景 | 策略 |
|------|------|
| LLM 服务不可用 | 降级为关键词匹配，前端提示"智能服务暂时不可用" |
| 推荐结果为空 | 提示"暂无匹配案例，请在知识库中手动搜索" |
| 模块识别失败 | 列出所有模块供手动选择 |
| 数据库连接异常 | 前端提示"服务暂时不可用，请稍后重试" |
| 权限不足 | 统一拦截，跳转 403 页面 |
| 网络超时 | 自动重试 3 次，超时后提示用户 |
| 附件上传超限 | 提示文件大小或类型限制，引导压缩后上传 |
| 存储空间不足 | 提示管理员扩容，暂停新附件上传 |

---

## 8. 部署方案

### 8.1 开发环境

```yaml
# docker-compose.yml
services:
  mysql:
    image: mysql:8.0
    ports: ["3306:3306"]
    environment:
      MYSQL_DATABASE: engineer_support
      MYSQL_USER: dev
      MYSQL_PASSWORD: dev
      MYSQL_ROOT_PASSWORD: root

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: mysql+aiomysql://dev:dev@mysql:3306/engineer_support
      LLM_API_KEY: ${LLM_API_KEY}
      LLM_API_BASE: ${LLM_API_BASE}
    depends_on: [mysql]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
```

### 8.2 生产环境

- MySQL 独立部署（云托管 RDS 或自建）
- 后端多实例 + Nginx 负载均衡
- 前端构建产物部署到 Nginx/CDN
- 环境变量配置 LLM API 密钥

---

## 9. 扩展性预留

1. **多来源工单接入** — adapter 模式，新增来源实现 adapter 接口即可
2. **多 LLM 支持** — LLM Client 抽象接口，可切换不同模型供应商
3. **向量检索升级** — 当前用 MySQL FULLTEXT 全文检索，未来可平滑接入 Milvus/Chroma 提升相似度匹配精度
4. **国际化** — 前端预留 i18n 框架
5. **通知集成** — 预留 webhook/邮件通知接口，工单状态变更时通知相关人员

---

## 10. 后续迭代规划

| 阶段 | 内容 |
|------|------|
| MVP | 工单 CRUD（含附件上传）、客户与部署实例管理、智能定位基础（LLM 模块/部署模式识别 + 关键词匹配）、案例沉淀、知识库搜索 |
| V2 | 多渠道工单接入、排查路径模板管理（按部署模式）、统计仪表盘 |
| V3 | 向量检索、案例自动标签、趋势分析、通知集成、附件在线预览 |
