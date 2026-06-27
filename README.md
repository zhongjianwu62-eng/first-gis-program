# 厦门市思明区路网结构与可步行性分析平台

本项目是 GIS 工程与开发课程设计的企业级工程化实现，研究范围为福建省厦门市思明区，并包含鼓浪屿。项目目标是建设一套面向城市规划人员、交通研究者和 GIS 分析人员的路网结构与可步行性分析工作台。

## 当前阶段

当前处于 D6：工程骨架搭建。

D6 的目标是建立可持续开发的基础工程结构，包括前端、后端、数据处理、数据库、部署和审计文档。D6 不接入真实 GIS 数据，不加载真实底图，不执行 PostGIS 查询。

## 技术方向

- 前端：Vue 3 + TypeScript + Vite
- 后端：FastAPI
- 数据库：PostgreSQL + PostGIS
- 数据处理：Python Pipeline
- 部署：Docker Compose + Nginx
- 数据来源：OpenStreetMap 路网数据
- 默认底图：天地图，OSM 备用，本地离线兜底

## 目录结构

```text
frontend/   前端 GIS 工作台
backend/    FastAPI 只读查询服务
pipeline/   离线数据处理工程
database/   数据库迁移和初始化
deploy/     部署配置
tests/      跨模块测试
docs/       需求、设计、审计和工作日志
```

## 本地开发入口

前端：

```text
cd frontend
npm install
npm run dev
```

后端：

```text
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```

PostGIS：

```text
cd deploy
docker compose up -d postgis
```

## 配置与凭证

仓库只提交 `.env.example`，不提交真实 `.env`。

天地图 token 必须通过本地环境变量或本地配置文件提供：

```text
VITE_TIANDITU_TOKEN=
```

真实 token 不得提交到 GitHub。

## GitHub 审计流程

每天工作应至少保留：

1. 功能分支；
2. 工作日志；
3. 审计报告；
4. Git 提交；
5. GitHub Pull Request。

## 下一步

D7 建议进入基础运行验证与开发环境完善，包括安装依赖、启动前端、启动后端、验证 `/health` 与 `/api/v1/meta`，并根据 D5 数据方案准备 Pipeline 输入。
