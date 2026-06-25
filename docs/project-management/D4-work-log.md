# D4 工作记录：模块拆分与详细设计

日期：2026-06-25
分支：`docs/d4-module-design`

## 当日目标

将 D3 总体架构转化为可执行的模块设计，明确系统模块、前端组件、后端服务、API 契约草案和数据库表结构草案，为 D5 数据源审计和 D6 工程骨架搭建提供输入。

## 已确认决策

| 决策项 | 结果 |
|---|---|
| 系统模块 | `frontend`、`backend`、`pipeline`、`database`、`deploy`、`tests`、`docs` |
| 前端结构 | 页面布局、地图模块、控制面板、详情面板、图表、搜索、导出、API、状态管理 |
| 地图模块 | `src/map` 集中管理初始化、图层、样式和交互 |
| 前端状态 | Pinia 按地图、图层、指标、选择、查询和系统状态拆分 |
| 后端结构 | `router → service → repository → database` |
| 后端职责 | 首版只读查询，不执行重型 GIS 计算，不提供业务数据写入接口 |
| API 前缀 | `/api/v1` |
| API 格式 | 地图几何返回 GeoJSON，统计和详情返回 JSON |
| API 错误 | 统一 `error_code`、`message`、`request_id` |
| 数据库核心表 | 8 张：数据版本、Pipeline 运行、指标定义、道路、节点、网格、网格指标、道路指标 |
| 指标字段策略 | 高频字段结构化，扩展指标 jsonb 化 |
| 坐标策略 | API 输出 EPSG:4326，米制指标由 Pipeline 在适合厦门的投影坐标下预计算 |

## 用户确认记录

1. 用户确认进入 D4 模块拆分与详细设计。
2. 用户确认系统模块拆分。
3. 用户确认前端组件拆分。
4. 用户确认后端服务拆分。
5. 用户确认 API 契约草案。
6. 用户确认继续进入数据库表结构草案和 D4 收尾。
7. 用户要求整理并提交 D4 文档。

## 完成内容

1. 明确工程根目录按 `frontend`、`backend`、`pipeline`、`database`、`deploy`、`tests`、`docs` 拆分。
2. 明确前端 `src` 目录按 `app`、`pages`、`layouts`、`components`、`features`、`stores`、`api`、`map`、`charts`、`utils`、`types`、`assets` 拆分。
3. 明确 GIS 工作台页面由顶部栏、左侧控制面板、地图主视图和右侧详情面板组成。
4. 明确地图模块的图层、样式和交互文件边界。
5. 明确搜索、导出、图表和详情面板作为独立 feature。
6. 明确 API 请求统一进入 `src/api`，组件不直接拼接 URL。
7. 明确 Pinia store 拆分。
8. 明确后端目录和 `router → service → repository → database` 分层。
9. 明确 Repository 层集中处理 PostGIS 查询，所有查询必须参数化。
10. 明确 API 契约草案，包括 meta、indicators、grids、roads、statistics、rankings 和 export。
11. 明确统一错误结构和错误码。
12. 明确 8 张数据库核心表及字段方向。
13. 明确数据版本、Pipeline 运行记录和指标定义作为审计核心。
14. 明确空间索引、字段索引和数据约束方向。
15. 明确 D5 与 D6 的后续任务输入。

## 审计重点

- D4 只做模块设计和契约草案，不直接写业务代码。
- D4 不新增 D2 未确认的大型功能。
- 首版仍保持匿名只读、固定公开权重和路网结构层面的可步行性评价。
- 后端首版只读，Pipeline 负责写数据库。
- 所有正式业务数据必须绑定数据版本。
- API 契约和数据库草案允许在实现阶段小幅调整，但不得破坏核心语义。
- 提交前需确认远端 main 已包含 D3 合并结果。

## 当日产物

- `docs/design/D4-module-design.md`
- `docs/design/D4-api-contract-draft.md`
- `docs/project-management/D4-work-log.md`
- `docs/audits/D4-design-audit.md`

## 遗留事项

- D5 需要审计思明区行政边界来源、OSM 数据获取方式、鼓浪屿覆盖、路网筛选规则和坐标系统。
- D6 需要根据 D4 目录设计搭建工程骨架。
- D6/D7 实现 API 和数据库时，可根据数据审计结果微调字段，但需要记录原因。

## D4 结论

D4 已将 D3 总体架构细化为可执行的模块设计、API 契约草案和数据库表结构草案。该设计与 D1、D2、D3 保持一致，可以进入 D5 数据源审计和 D6 工程骨架搭建。
