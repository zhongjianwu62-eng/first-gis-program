# D4 模块拆分与详细设计

## 厦门市思明区城市路网结构与可步行性分析平台

| 项目属性 | 内容 |
|---|---|
| 文档版本 | 1.0 |
| 日期 | 2026-06-25 |
| 上游输入 | D1 项目章程、D2 需求分析、D3 总体架构 |
| 研究区域 | 福建省厦门市思明区，包含鼓浪屿 |
| 设计阶段 | D4 模块拆分与详细设计 |
| 状态 | 已整理，待审计、提交与线上留痕 |

## 1. D4 目标

D4 的目标是将 D3 总体架构细化为可执行的模块设计，明确工程目录、前端组件、后端分层、API 契约方向和数据库表结构草案。

D4 不直接写业务代码，但必须让后续 D5 数据源审计和 D6 工程骨架搭建有明确输入。

## 2. 系统模块拆分

项目采用模块化单体工程结构，建议根目录按以下方式组织：

```text
first-gis-program
├── frontend        Vue 3 GIS 工作台
├── backend         FastAPI 查询服务
├── pipeline        离线数据处理工程
├── database        数据库迁移、初始化 SQL、PostGIS 扩展
├── docs            项目文档、需求、设计、审计、工作日志
├── deploy          Docker Compose、Nginx、生产部署配置
└── tests           跨模块测试或端到端测试
```

| 模块 | 职责 |
|---|---|
| `frontend` | 地图展示、图层控制、指标切换、搜索、详情面板、图表、导出入口 |
| `backend` | API 接口、参数校验、业务规则、数据库查询、错误处理、日志 |
| `pipeline` | 获取数据、清洗道路、构建路网、计算指标、写入 PostGIS |
| `database` | 表结构迁移、索引、PostGIS 扩展、初始化指标定义 |
| `docs` | 需求、架构、设计、审计、每日工作记录 |
| `deploy` | 本地和生产部署配置 |
| `tests` | 端到端测试、接口测试、关键业务流程测试 |

模块关系如下：

```text
frontend
   ↓ 调用 /api/v1
backend
   ↓ 查询
database / PostGIS

pipeline
   ↓ 写入正式数据版本
database / PostGIS

deploy
   ↓ 运行
frontend + backend + database

docs
   ↓ 记录
所有需求、设计、审计和每日进度
```

关键边界：

1. `pipeline` 可以写数据库；
2. `backend` 首版只读数据库；
3. `frontend` 永远不直接访问数据库；
4. `docs` 记录所有关键设计、审计和每日工作；
5. `deploy` 只管理运行环境，不承载业务逻辑。

## 3. 前端组件拆分

前端采用 Vue 3 + TypeScript + Pinia + MapLibre GL JS + Element Plus + ECharts。

建议目录结构：

```text
frontend
└── src
    ├── app                  应用入口与全局配置
    ├── pages                页面级组件
    ├── layouts              工作台布局
    ├── components           通用 UI 组件
    ├── features             业务功能模块
    ├── stores               Pinia 状态管理
    ├── api                  后端接口调用
    ├── map                  地图初始化、图层、样式、交互
    ├── charts               图表配置
    ├── utils                工具函数
    ├── types                TypeScript 类型
    └── assets               静态资源
```

### 3.1 页面与布局

首版核心页面为：

```text
pages/WorkbenchPage.vue
```

页面组件只负责组装布局：

```text
WorkbenchPage
├── AppHeader
├── WorkbenchLayout
│   ├── LeftControlPanel
│   ├── MapCanvas
│   └── RightInsightPanel
```

| 组件 | 职责 |
|---|---|
| `WorkbenchPage` | GIS 工作台页面容器 |
| `AppHeader` | 顶部栏，展示系统名称、数据版本、导出和帮助入口 |
| `LeftControlPanel` | 指标选择、图层开关、筛选条件 |
| `MapCanvas` | 地图主视图 |
| `RightInsightPanel` | 指标解释、网格详情、道路详情、排行榜和图表 |

页面层不负责复杂业务逻辑和数据计算。

### 3.2 地图模块

地图相关代码集中在 `src/map`：

```text
map
├── initMap.ts              初始化 MapLibre 地图
├── layers
│   ├── boundaryLayer.ts    思明区边界图层
│   ├── gridLayer.ts        500 米网格图层
│   ├── roadLayer.ts        道路图层
│   └── highlightLayer.ts   高亮图层
├── styles
│   ├── gridStyle.ts        网格分级设色
│   └── roadStyle.ts        道路样式
└── interactions
    ├── clickGrid.ts        点击网格
    ├── clickRoad.ts        点击道路
    └── moveViewport.ts     地图移动后触发 bbox 查询
```

地图模块负责初始化地图、添加图层、更新图层数据、处理点击、根据指标更新颜色、地图移动后触发 bbox 查询。

地图模块不写死接口地址，不解释指标含义，不直接操作右侧面板，不独立保存全部业务状态。地图交互产生的选择结果写入 Pinia。

### 3.3 左侧控制面板

左侧控制面板放入 `features/control-panel`：

```text
control-panel
├── IndicatorSelector.vue
├── LayerToggle.vue
├── RoadNetworkFilter.vue
├── ClassificationSelector.vue
└── FilterResetButton.vue
```

左侧面板负责当前指标、图层、道路网络类型、分级方式和筛选条件。它不直接查询数据库，也不直接操作地图图层，只改变状态。

### 3.4 右侧详情面板

右侧详情面板放入 `features/insight-panel`：

```text
insight-panel
├── IndicatorDescription.vue
├── OverviewCards.vue
├── GridDetailPanel.vue
├── RoadDetailPanel.vue
├── RankingList.vue
└── EmptyInsightState.vue
```

右侧面板负责解释指标、展示全区概览、展示网格详情、展示道路详情、展示高值和低值榜单，并用图表辅助理解。

### 3.5 图表模块

图表配置放入 `src/charts`：

```text
charts
├── indicatorBarChart.ts
├── gridRadarChart.ts
└── distributionChart.ts
```

图表组件放入 `components/charts`：

```text
components/charts
├── BaseEChart.vue
├── IndicatorBarChart.vue
├── GridRadarChart.vue
└── DistributionChart.vue
```

ECharts 初始化、resize 和销毁逻辑集中封装，业务组件只传入数据。

### 3.6 搜索与导出

道路搜索放入 `features/search`：

```text
search
├── RoadSearchBox.vue
├── SearchResultList.vue
└── useRoadSearch.ts
```

CSV 导出放入 `features/export`：

```text
export
├── ExportButton.vue
└── useExportCsv.ts
```

搜索和导出作为独立业务能力，不塞入地图组件。

### 3.7 API 模块

所有后端请求统一放在 `src/api`：

```text
api
├── httpClient.ts
├── metaApi.ts
├── gridApi.ts
├── roadApi.ts
├── indicatorApi.ts
├── rankingApi.ts
└── exportApi.ts
```

组件不直接拼接 URL，只调用 API 方法。

### 3.8 Pinia 状态拆分

```text
stores
├── useMapStore.ts
├── useLayerStore.ts
├── useIndicatorStore.ts
├── useSelectionStore.ts
├── useQueryStore.ts
└── useSystemStore.ts
```

| Store | 职责 |
|---|---|
| `useMapStore` | 地图中心点、缩放级别、bbox |
| `useLayerStore` | 网格、道路、节点、边界是否显示 |
| `useIndicatorStore` | 当前指标、分级方式、指标定义 |
| `useSelectionStore` | 当前选中网格、道路、搜索结果 |
| `useQueryStore` | 加载中、失败、空结果、请求状态 |
| `useSystemStore` | 数据版本、研究区、系统配置 |

### 3.9 类型定义

TypeScript 类型放入 `src/types`：

```text
types
├── api.ts
├── map.ts
├── grid.ts
├── road.ts
├── indicator.ts
├── ranking.ts
└── system.ts
```

前端组件不直接理解数据库字段，只使用 API 返回结构和前端类型。

## 4. 后端服务拆分

后端采用 FastAPI，定位为只读 GIS 查询服务。

建议目录结构：

```text
backend
├── app
│   ├── main.py
│   ├── api
│   │   └── v1
│   │       ├── router.py
│   │       ├── meta.py
│   │       ├── grids.py
│   │       ├── roads.py
│   │       ├── indicators.py
│   │       ├── rankings.py
│   │       └── export.py
│   ├── core
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── errors.py
│   │   └── security.py
│   ├── schemas
│   │   ├── common.py
│   │   ├── grid.py
│   │   ├── road.py
│   │   ├── indicator.py
│   │   ├── ranking.py
│   │   └── meta.py
│   ├── services
│   │   ├── grid_service.py
│   │   ├── road_service.py
│   │   ├── indicator_service.py
│   │   ├── ranking_service.py
│   │   └── export_service.py
│   ├── repositories
│   │   ├── grid_repository.py
│   │   ├── road_repository.py
│   │   ├── indicator_repository.py
│   │   ├── ranking_repository.py
│   │   └── meta_repository.py
│   ├── database
│   │   ├── session.py
│   │   ├── models.py
│   │   └── spatial.py
│   └── utils
│       ├── bbox.py
│       ├── pagination.py
│       └── csv.py
└── tests
    ├── unit
    └── integration
```

### 4.1 后端分层

后端采用：

```text
router → service → repository → database
```

| 层 | 职责 |
|---|---|
| router | 接收 HTTP 请求，绑定路径，调用 service，返回响应 |
| service | 处理业务规则，例如 bbox 限制、导出数量限制、数据版本选择 |
| repository | 封装数据库查询，尤其是 PostGIS 空间查询 |
| database | 管理数据库连接、模型、空间辅助函数 |
| schemas | 定义请求参数和响应结构 |
| core | 管理配置、日志、错误、安全边界 |

### 4.2 Router 层

`api/v1` 负责接口入口：

```text
api/v1/meta.py
api/v1/grids.py
api/v1/roads.py
api/v1/indicators.py
api/v1/rankings.py
api/v1/export.py
```

Router 层只接收参数、调用 service、返回结果，不直接写 SQL，不处理复杂业务规则。

### 4.3 Service 层

Service 层负责业务规则，例如 bbox 是否过大、导出数量是否超限、当前数据版本如何确定、空结果如何返回、指标编码是否有效。

### 4.4 Repository 层

Repository 层负责数据库查询，包括 SQLAlchemy 查询、GeoAlchemy2、PostGIS 函数和参数化 SQL。

所有数据库查询必须参数化，不允许把前端传入字符串直接拼入 SQL。

### 4.5 Schema 层

`schemas` 使用 Pydantic 定义请求和响应结构，例如 `BBoxQuery`、`GridFeature`、`GridDetailResponse`、`RoadSearchResponse`、`IndicatorDefinition` 和 `ErrorResponse`。

### 4.6 Database 层

```text
database/session.py
database/models.py
database/spatial.py
```

`session.py` 管理数据库连接和会话，`models.py` 管理表模型，`spatial.py` 管理 bbox、坐标和 GeoJSON 转换等空间辅助逻辑。

### 4.7 Core 与 Utils

`core` 管理配置、日志、错误和安全边界。`utils` 只放纯工具函数，例如 bbox 解析、分页限制和 CSV 生成。

## 5. 数据库表结构草案

数据库采用 PostgreSQL + PostGIS，首版围绕 8 张核心表设计：

```text
data_versions
pipeline_runs
indicator_definitions
roads
road_nodes
analysis_grids
grid_indicators
road_indicators
```

### 5.1 `data_versions`

记录每一版正式数据。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `version_code` | text | 版本号 |
| `study_area_name` | text | 研究区名称 |
| `source_name` | text | 数据来源 |
| `source_snapshot_at` | timestamp | 数据获取时间 |
| `pipeline_version` | text | Pipeline 脚本版本 |
| `indicator_version` | text | 指标算法版本 |
| `is_current` | boolean | 是否当前启用版本 |
| `created_at` | timestamp | 创建时间 |
| `notes` | text | 备注 |

### 5.2 `pipeline_runs`

记录每一次离线处理过程。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 关联数据版本 |
| `status` | text | 运行状态 |
| `started_at` | timestamp | 开始时间 |
| `finished_at` | timestamp | 结束时间 |
| `input_source` | text | 输入数据来源 |
| `input_boundary` | text | 行政边界来源 |
| `script_version` | text | 脚本版本 |
| `records_summary` | jsonb | 生成记录数量摘要 |
| `log_summary` | text | 日志摘要 |
| `error_message` | text | 错误摘要 |

### 5.3 `indicator_definitions`

存储指标元数据。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 关联数据版本 |
| `code` | text | 指标编码 |
| `name_zh` | text | 中文名 |
| `name_en` | text | 英文名 |
| `description` | text | 指标解释 |
| `unit` | text | 单位 |
| `direction` | text | `positive` 或 `negative` |
| `weight` | numeric | 权重 |
| `is_composite` | boolean | 是否综合指标 |
| `display_order` | integer | 展示顺序 |

### 5.4 `roads`

存储清洗后的道路几何和基础属性。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 数据版本 |
| `road_code` | text | 系统内部道路编号 |
| `source_osm_id` | text | OSM 来源 ID |
| `name` | text | 道路名称 |
| `road_class` | text | 道路等级 |
| `is_motor_accessible` | boolean | 是否机动车可通行 |
| `is_walk_accessible` | boolean | 是否步行可通行 |
| `length_m` | numeric | 道路长度，米 |
| `geom` | geometry(LineString/MultiLineString, 4326) | 道路几何 |
| `created_at` | timestamp | 创建时间 |

### 5.5 `road_nodes`

存储道路网络节点。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 数据版本 |
| `node_code` | text | 节点编号 |
| `network_type` | text | `motor` 或 `walk` |
| `degree` | integer | 连接道路数量 |
| `is_intersection` | boolean | 是否交叉口 |
| `geom` | geometry(Point, 4326) | 节点几何 |
| `created_at` | timestamp | 创建时间 |

### 5.6 `analysis_grids`

存储 500 米分析网格。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 数据版本 |
| `grid_code` | text | 网格编号 |
| `study_area_name` | text | 所属研究区 |
| `center_lng` | numeric | 中心点经度 |
| `center_lat` | numeric | 中心点纬度 |
| `area_m2` | numeric | 网格面积 |
| `is_boundary_grid` | boolean | 是否边界网格 |
| `is_included_in_stats` | boolean | 是否参与统计 |
| `geom` | geometry(Polygon/MultiPolygon, 4326) | 网格几何 |
| `created_at` | timestamp | 创建时间 |

### 5.7 `grid_indicators`

存储网格级可步行性分析结果。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 数据版本 |
| `grid_id` | UUID | 关联网格 |
| `walkability_score` | numeric | 综合可步行性分数 |
| `rank_percentile` | numeric | 全区百分位 |
| `class_level` | integer | 分级等级 |
| `indicator_values` | jsonb | 各指标原始值 |
| `normalized_values` | jsonb | 各指标标准化值 |
| `district_averages` | jsonb | 全区均值对比 |
| `interpretation` | text | 简短解释文本 |
| `created_at` | timestamp | 创建时间 |

### 5.8 `road_indicators`

存储道路级分析结果。

| 字段 | 类型方向 | 说明 |
|---|---|---|
| `id` | UUID | 主键 |
| `data_version_id` | UUID | 数据版本 |
| `road_id` | UUID | 关联道路 |
| `network_type` | text | `motor` 或 `walk` |
| `betweenness_centrality` | numeric | 边介数中心性 |
| `degree_related_score` | numeric | 连接相关指标 |
| `indicator_values` | jsonb | 其他道路级指标 |
| `created_at` | timestamp | 创建时间 |

### 5.9 表关系

```text
data_versions
   ├── pipeline_runs
   ├── indicator_definitions
   ├── roads
   │     └── road_indicators
   ├── road_nodes
   └── analysis_grids
         └── grid_indicators
```

### 5.10 索引与约束

首版至少建立：

- `data_versions.version_code` 唯一索引；
- `data_versions.is_current` 索引；
- `roads.geom` GiST 空间索引；
- `analysis_grids.geom` GiST 空间索引；
- `road_nodes.geom` GiST 空间索引；
- `roads.name` 索引；
- `roads.road_class` 索引；
- `grid_indicators.walkability_score` 索引；
- `grid_indicators.rank_percentile` 索引；
- `road_indicators.betweenness_centrality` 索引；
- `indicator_definitions.code` 索引。

数据库约束：

1. 所有业务表必须有 `data_version_id`；
2. 所有正式几何数据必须有 SRID；
3. `grid_code` 在同一数据版本内唯一；
4. `road_code` 在同一数据版本内唯一；
5. 指标编码在同一数据版本内唯一；
6. 一个网格在同一版本内只能有一条综合指标结果；
7. 一条道路在同一版本和网络类型下只能有一条指标结果；
8. 当前启用版本只能有一个；
9. Pipeline 失败版本不能设为当前启用版本；
10. 删除旧数据版本必须通过人工审计。

### 5.11 坐标系统策略

- API 输出使用 `EPSG:4326`；
- 数据库正式几何字段首版使用 `EPSG:4326`；
- 米制长度、面积、密度等指标由 Pipeline 在适合厦门的投影坐标下计算后写入；
- D5 专门验证 `EPSG:32650` 是否作为正式计算投影；
- 前端地图使用经纬度数据渲染。

### 5.12 指标字段策略

网格指标采用“高频字段结构化 + 扩展指标 jsonb 化”的混合模式：

- 高频查询字段单独列出，例如 `walkability_score`、`rank_percentile`、`class_level`；
- 可扩展单项指标放入 `indicator_values` 和 `normalized_values`；
- 指标解释由 `indicator_definitions` 管理；
- 后续若某个指标变成高频排序字段，再提升为正式列。

## 6. D4 边界原则

1. D4 不新增 D2 未确认的大型功能；
2. 前端不直接访问数据库；
3. 后端首版只读，不提供业务数据新增、修改、删除接口；
4. Pipeline 负责写入正式数据版本；
5. 所有正式结果必须绑定数据版本；
6. 地图数据按 bbox 查询；
7. 数据库查询必须参数化；
8. API 契约和数据库表结构在 D6/D7 实现时可小幅调整，但不得破坏核心语义。

## 7. D4 结论

D4 将 D3 总体架构细化为可执行的模块设计。系统按 `frontend`、`backend`、`pipeline`、`database`、`deploy`、`tests` 和 `docs` 拆分；前端按页面、地图、控制面板、详情面板、图表、搜索、导出、API 和状态管理组织；后端按 router、service、repository、database、schemas、core 和 utils 分层；数据库围绕数据版本、Pipeline 运行、指标定义、道路、节点、网格和指标结果建立表结构草案。

D4 可以作为 D5 数据源审计和 D6 工程骨架搭建的输入。
