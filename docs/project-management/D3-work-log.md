# D3 工作记录：总体架构设计

日期：2026-06-23
分支：`docs/d3-system-architecture`

## 当日目标

将 D1 项目章程和 D2 需求分析转化为可执行的总体架构蓝图，明确系统分层、技术选型、数据流、API 边界、数据库版本治理、前端工作台设计、部署策略和高并发演进路线。

## 已确认决策

| 决策项 | 结果 |
|---|---|
| 总体架构 | 模块化单体架构 |
| 核心链路 | Vue 3 前端 + FastAPI 后端 + PostGIS 数据库 + 离线 Pipeline |
| 前端地图引擎 | MapLibre GL JS |
| 前端工程 | Vue 3 + TypeScript + Composition API + Pinia |
| UI 与图表 | Element Plus 基础控件 + 自定义 GIS 工作台视觉 + ECharts |
| 后端框架 | FastAPI |
| 后端访问数据库 | SQLAlchemy 2.0 + GeoAlchemy2，复杂空间查询允许参数化 SQL |
| API 返回 | 地图几何使用 GeoJSON，统计和详情使用 JSON |
| API 版本 | `/api/v1` |
| 地图数据加载 | 按当前地图视野 bbox 查询 |
| 数据库 | PostgreSQL + PostGIS |
| 数据版本 | `data_versions` 管理正式数据版本 |
| Pipeline | 独立 Python 数据处理工程，离线运行后写入 PostGIS |
| 后端分层 | `router → service → repository → database` |
| Redis | 首版不引入，保留缓存边界 |
| 部署 | 首版单台云服务器 + Docker Compose + Nginx + HTTPS |
| 自动审计 | GitHub Actions 运行格式、类型、测试、构建和敏感信息扫描 |
| 测试工具 | Vitest + pytest + Playwright |

## 用户确认记录

1. 用户确认继续采用 20 天企业级路线推进项目。
2. 用户确认 D3 采用模块化单体架构，不采用过重的微服务路线。
3. 用户确认总体架构为“Vue 3 GIS 工作台 → FastAPI 查询服务 → PostGIS → 离线 Pipeline”。
4. 用户确认技术选型：Vue 3、TypeScript、Pinia、MapLibre、FastAPI、PostGIS、Pipeline、Docker Compose。
5. 用户确认系统数据流与模块边界。
6. 用户确认 API 与数据访问设计。
7. 用户确认数据库与数据版本设计，并继续进入前端工作台设计。
8. 用户确认前端 GIS 工作台设计。
9. 用户确认部署、运维与高并发演进设计。
10. 用户确认进入最后一块风险、验收标准与审计计划。
11. 用户要求开始整理 D3 正式文档。

## 完成内容

1. 明确总体架构采用模块化单体，而不是静态网页、过早微服务或 Kubernetes 架构。
2. 明确系统由前端 GIS 工作台、FastAPI 查询服务、PostGIS 数据库和离线 Pipeline 四个核心模块组成。
3. 明确前端采用 Vue 3 + TypeScript + Pinia + MapLibre GL JS + Element Plus + ECharts。
4. 明确后端采用 FastAPI + Pydantic + SQLAlchemy 2.0 + GeoAlchemy2 + Alembic。
5. 明确数据库采用 PostgreSQL + PostGIS，GeoJSON 仅作为接口输出格式，不作为正式主存储。
6. 明确 Pipeline 负责数据获取、清洗、建图、指标计算、入库和版本记录。
7. 明确 API 采用 `/api/v1` 版本化 REST 风格，只读查询为主。
8. 明确道路和网格查询必须支持 bbox 范围过滤。
9. 明确后端内部采用 router、service、repository、database 分层。
10. 明确数据库核心表包括 `data_versions`、`roads`、`road_nodes`、`analysis_grids`、`grid_indicators`、`road_indicators`、`indicator_definitions` 和 `pipeline_runs`。
11. 明确数据版本发布规则：只有完整处理并通过校验的数据版本才能成为当前启用版本。
12. 明确前端采用顶部栏、左侧控制面板、地图主视图和右侧详情面板的 GIS 工作台布局。
13. 明确首版部署采用单台云服务器 + Docker Compose + Nginx + HTTPS。
14. 明确商业化高并发演进路线：单机优化、Redis 缓存、后端横向扩展、数据库读写分离、矢量瓦片/CDN、容器编排与监控体系。
15. 明确 D3 风险、范围边界、验收标准和审计计划。

## 审计重点

- D3 不新增 D2 未确认的大型首版功能。
- 首版仍保持匿名只读，不引入登录和权限系统。
- 首版仍使用固定公开权重，不引入在线权重编辑。
- 首版仍聚焦路网结构层面的可步行性潜力评价，不纳入 POI 和设施可达性。
- 首版不引入 Redis、微服务、Kubernetes 和 MVT，但保留演进边界。
- 数据版本和 Pipeline 运行记录作为企业级审计核心。
- 地图加载和 API 查询必须避免一次性加载全区详细几何。
- D3 输出必须能支撑 D4 模块拆分、D5 数据源审计和 D6 工程搭建。

## 当日产物

- `docs/architecture/D3-system-architecture.md`
- `docs/project-management/D3-work-log.md`
- `docs/audits/D3-architecture-audit.md`

## 遗留事项

- D4 需要在 D3 架构基础上拆分系统模块、接口契约、数据库草图和页面组件。
- D5 需要验证正式行政边界、OSM 数据获取方式、坐标系统和数据质量。
- D6 需要开始搭建工程骨架，并建立前端、后端、数据库和 Pipeline 的基础目录。
- GitHub 远端 `main` 与本地 D2 合并状态需要在推送 D3 前再次核对，避免重复合并或分支基线错位。

## D3 结论

D3 总体架构已经形成可执行蓝图。该架构与 D1 项目章程一致，覆盖 D2 已确认需求，能够支撑后续模块拆分、数据审计、工程搭建和企业级 GitHub 留痕流程。
