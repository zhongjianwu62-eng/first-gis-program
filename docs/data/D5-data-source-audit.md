# D5 数据源审计说明

## 厦门市思明区城市路网结构与可步行性分析平台

| 项目属性 | 内容 |
|---|---|
| 文档版本 | 1.0 |
| 日期 | 2026-06-27 |
| 上游输入 | D1 项目章程、D2 需求分析、D3 总体架构、D4 模块设计 |
| 研究区域 | 福建省厦门市思明区，包含鼓浪屿 |
| 审计主题 | 行政边界、路网数据、底图合规、坐标系统、数据质量 |
| 状态 | 已整理，待提交与线上留痕 |

## 1. D5 目标

D5 的目标是建立正式数据方案和数据质量审计规则，为后续 Pipeline 开发、PostGIS 入库、指标计算和前端展示提供可信数据基线。

D5 不直接下载正式数据，也不写 Pipeline 代码。D5 的交付重点是明确：

1. 研究范围与行政边界来源策略；
2. 底图选择与天地图凭证管理规则；
3. OSM 路网数据来源与版本记录规则；
4. 机动车路网与步行路网筛选规则；
5. 坐标系统与米制计算策略；
6. 数据质量审计指标和风险分级。

## 2. 研究范围与行政边界

正式研究范围为：

```text
福建省厦门市思明区，包含鼓浪屿
```

行政边界必须满足：

1. 完整覆盖厦门岛内思明区主体；
2. 完整包含鼓浪屿；
3. 不人为创建厦门岛主体与鼓浪屿之间的虚假道路连接；
4. 能用于裁剪道路、生成 500 米网格和识别边界网格；
5. 来源、获取时间、许可说明和处理方式可记录、可复现。

候选边界来源按以下方式审计：

| 来源 | 用途 | 风险 |
|---|---|---|
| 官方行政区划边界 | 最理想的正式边界来源 | 获取难度可能较高，格式可能不统一 |
| OpenStreetMap 行政边界 | 容易和 OSM 路网配套 | 边界准确性需要核查 |
| 公开 GeoJSON / GADM / 其他公开边界 | 可作为对照或兜底 | 许可、精度、更新日期需要审计 |

D5 建议采用“主边界源 + 辅助对照源”的方式，不直接依赖单一来源。首版可使用可复现获取的思明区行政边界作为主边界，并使用 OSM 或其他公开边界进行空间对照。

鼓浪屿作为思明区的一部分进入研究范围。鼓浪屿道路、网格和指标应纳入分析，但其路网连通关系必须保持真实。如果鼓浪屿形成独立网络子图，这是正常地理事实，不是数据错误。

## 3. 底图选择与天地图凭证管理

底图是地图背景层，不作为路网分析指标的数据来源。首版底图策略为：

```text
默认底图：天地图
备用底图：OpenStreetMap
离线兜底：简化本地底图或空白底图
```

天地图作为优先推荐底图，适合国内区域展示和教学科研场景。系统同时保留 OSM 备用底图和离线兜底，避免对单一底图服务形成硬依赖。

底图接入规则：

1. 天地图开发者凭证通过官网申请；
2. 真实凭证不得写死在代码中；
3. 真实凭证不得提交到公开仓库；
4. 仓库只提交 `.env.example`；
5. 本地真实配置放入 `.env.local` 或 `.env`；
6. 前端通过环境变量读取底图凭证；
7. 底图服务地址和凭证统一由底图配置层管理，不散落在 Vue 组件中。

`.env.example` 仅保留空配置示例：

```text
VITE_TIANDITU_TOKEN=
```

前端底图配置建议包括：

```text
tianditu.vector
tianditu.image
tianditu.terrain
tianditu.annotation
osm.standard
offline.blank
```

如果 OSM 道路与天地图底图出现视觉偏移，必须作为数据审计问题记录。首版不得未经说明私自修改分析数据坐标。

## 4. OSM 路网数据来源

本项目首版路网分析数据来源采用 OpenStreetMap。底图服务不作为分析数据源。

候选获取方式如下：

| 方案 | 说明 | 优点 | 风险 |
|---|---|---|---|
| OSMnx | 用 Python 按行政边界或边界几何下载 OSM 路网 | 开发效率高，适合教学和研究 | 依赖网络和 Overpass 服务稳定性 |
| Overpass API | 直接写 Overpass 查询获取道路 | 可控性强，查询条件清楚 | 查询语句复杂，容易超时 |
| OSM PBF 离线包 | 下载福建或中国 OSM PBF 后本地裁剪 | 稳定、可复现、适合企业化 | 首版工程复杂度更高 |

首版推荐：

```text
使用 OSMnx 获取思明区道路数据，并记录 Overpass 查询思路和未来 PBF 离线方案作为演进路线。
```

OSM 数据获取流程：

```text
思明区边界
   ↓
OSMnx / Overpass 获取道路
   ↓
按边界裁剪
   ↓
道路类型与访问属性筛选
   ↓
机动车路网 + 步行路网
   ↓
写入 PostGIS
```

每次获取 OSM 数据必须记录：

| 项 | 说明 |
|---|---|
| 数据来源 | OpenStreetMap |
| 获取方式 | OSMnx / Overpass |
| 获取时间 | 具体日期时间 |
| 研究范围 | 福建省厦门市思明区 |
| 边界来源 | D5 确认的边界源 |
| 网络类型 | 机动车路网、步行路网 |
| 原始记录数量 | 原始道路数量 |
| 清洗后数量 | 入库道路数量 |
| 坐标系统 | API 输出 EPSG:4326 |
| 许可说明 | 记录 OSM 数据来源与署名要求 |

前端或帮助说明中应保留道路数据来源说明：

```text
道路数据来源：OpenStreetMap contributors
```

首版采用固定时间快照，不直接依赖实时最新数据。后续如果重新获取 OSM 数据，应生成新的数据版本，不直接覆盖旧版本。

## 5. 机动车路网与步行路网筛选

首版从 OSM 原始道路中派生两套逻辑路网：

```text
机动车路网：用于分析城市道路骨架、关键道路、结构中心性
步行路网：用于分析路网结构层面的可步行性潜力
```

### 5.1 机动车路网

机动车路网建议纳入的 OSM `highway` 类型：

```text
motorway
trunk
primary
secondary
tertiary
unclassified
residential
service
living_street
```

建议排除：

```text
footway
pedestrian
path
steps
cycleway
track
bridleway
construction
proposed
```

机动车路网还需要结合访问属性判断。若出现以下属性，应排除或标记：

```text
access=no
motor_vehicle=no
vehicle=no
access=private
```

其中 `access=private` 建议默认不参与正式机动车网络，但保留审计记录。

### 5.2 步行路网

步行路网建议纳入的 OSM `highway` 类型：

```text
primary
secondary
tertiary
unclassified
residential
living_street
service
pedestrian
footway
path
steps
corridor
```

主次道路可以进入步行路网作为空间骨架，但不代表步行体验一定好。后续通过道路等级、访问属性和指标解释区分其步行友好程度。

建议谨慎纳入：

```text
cycleway
track
```

建议排除：

```text
motorway
trunk
construction
proposed
raceway
bridleway
```

步行路网应排除：

```text
access=no
foot=no
```

若 `foot=yes` 或 `foot=designated`，可以明确纳入步行网络。若缺失 `foot` 属性，则根据 `highway` 类型推断纳入，并记录为“推断纳入”。

### 5.3 特殊道路处理

`service` 道路可能是小区内部道路、停车场道路、单位内部道路、商业区服务道路或普通支路。首版规则为：

```text
机动车路网：纳入 service，但排除 access=private/no 的道路
步行路网：纳入 service，但标记为低等级道路
```

`footway`、`pedestrian`、`steps` 对步行路网很重要：

1. `footway` 纳入步行路网；
2. `pedestrian` 纳入步行路网；
3. `steps` 纳入步行路网，但单独标记；
4. `steps` 参与连通性，但在可步行性解释中说明其对无障碍步行不一定友好。

鼓浪屿道路纳入研究范围，不建立虚假的跨海道路连接。若鼓浪屿形成独立网络子图，应作为正常信息记录。

## 6. 坐标系统与米制计算

项目采用“经纬度存储与展示、米制投影计算”的策略。

| 场景 | 坐标系统 | 原因 |
|---|---|---|
| OSM 原始数据获取 | `EPSG:4326` | OSM 常用经纬度坐标 |
| PostGIS 正式几何存储 | `EPSG:4326` | API 和前端交换方便 |
| GeoJSON API 输出 | `EPSG:4326` | GeoJSON / Web 地图通用 |
| 前端地图渲染 | 经纬度输入，由地图引擎处理 | MapLibre 与底图体系适配 |
| 道路长度计算 | `EPSG:32650` | 单位为米 |
| 网格面积计算 | `EPSG:32650` | 单位为平方米 |
| 500 米网格生成 | `EPSG:32650` | 网格尺寸需要米制 |
| 路网密度计算 | `EPSG:32650` | km/km² 依赖长度和面积 |
| 交叉口密度计算 | `EPSG:32650` | 个/km² 依赖面积 |

`EPSG:4326` 的坐标单位是度，适合存储、接口、展示和空间交换，不适合直接计算米制长度、面积和密度。

`EPSG:32650` 属于 WGS 84 / UTM zone 50N，单位为米，覆盖厦门所在经度范围，适合作为首版米制计算投影。

Pipeline 坐标处理流程：

```text
读取 OSM / 边界数据 EPSG:4326
        ↓
统一检查 SRID
        ↓
投影到 EPSG:32650
        ↓
道路长度、面积、密度、500 米网格等米制计算
        ↓
生成计算结果字段
        ↓
几何转回 EPSG:4326
        ↓
写入 PostGIS
```

`EPSG:3857` 仅用于 Web 地图显示场景，不作为正式指标计算坐标系。

建议在数据版本或 Pipeline 记录中保存：

```text
source_crs = EPSG:4326
analysis_crs = EPSG:32650
storage_crs = EPSG:4326
api_crs = EPSG:4326
```

## 7. 数据质量审计规则

D5 数据质量审计目标不是追求数据完美，而是保证数据来源清楚、处理过程可复现、关键问题可发现、风险可解释。

审计对象包括：

| 对象 | 审计重点 |
|---|---|
| 行政边界 | 是否完整覆盖思明区和鼓浪屿 |
| 道路数据 | 是否在边界内、类型是否合理、是否重复 |
| 双路网 | 机动车路网和步行路网是否按规则生成 |
| 节点数据 | 交叉口、端点、孤立节点是否异常 |
| 500 米网格 | 是否覆盖研究区、边界网格是否标记 |
| 底图配置 | 天地图凭证是否合规、OSM/离线底图是否可兜底 |

### 7.1 行政边界审计

检查项：

1. 是否包含厦门岛内思明区主体；
2. 是否包含鼓浪屿；
3. 是否存在明显缺口、重叠或破碎面；
4. 边界几何是否合法；
5. 边界面积是否大致合理；
6. 边界来源、获取时间、许可说明是否记录；
7. 是否可以用于裁剪道路和生成 500 米网格。

### 7.2 道路数据审计

| 检查项 | 说明 |
|---|---|
| 空几何 | 道路是否存在空 geometry |
| 非法几何 | 是否有无法计算或自相交等异常 |
| 边界外道路 | 是否存在明显超出思明区边界的数据 |
| 重复道路 | 是否有完全重复或高度重叠道路 |
| 道路名称缺失 | 缺失名称可以接受，但要统计比例 |
| 道路类型缺失 | `highway` 缺失会影响分类，需重点记录 |
| 长度异常 | 是否存在过短或异常长道路 |
| 服务道路占比 | `service` 占比过高可能影响分析 |
| 私有/受限道路 | `access=private/no` 是否被正确标记或排除 |

### 7.3 鼓浪屿连通性审计

检查项：

1. 鼓浪屿是否在边界内；
2. 鼓浪屿道路是否被获取；
3. 鼓浪屿道路是否进入步行路网；
4. 鼓浪屿是否形成独立网络子图；
5. 是否存在错误的跨海道路连接；
6. 是否因为边界裁剪误删鼓浪屿道路；
7. 统计结果是否能解释“岛屿独立网络”现象。

### 7.4 节点和连通性审计

建议输出：

```text
motor_network_component_count
motor_largest_component_ratio
walk_network_component_count
walk_largest_component_ratio
intersection_count
dead_end_count
isolated_node_count
```

### 7.5 500 米网格审计

检查项：

1. 网格是否覆盖完整研究区；
2. 网格尺寸是否为 500 米；
3. 网格是否由米制投影生成；
4. 边界网格是否被标记；
5. 面积过小的边界网格是否可识别；
6. 鼓浪屿网格是否存在；
7. 每个网格是否能关联道路和指标；
8. 是否有完全无道路网格；
9. 是否记录 `is_boundary_grid` 和 `is_included_in_stats`。

### 7.6 审计等级

| 等级 | 含义 | 处理 |
|---|---|---|
| Blocker | 会导致分析结论不可用 | 必须修复后才能进入正式版本 |
| Warning | 会影响部分解释，但不阻塞首版 | 记录并在说明中解释 |
| Info | 正常数据特征或轻微问题 | 记录即可 |

示例：

- Blocker：思明区边界缺少鼓浪屿；
- Blocker：道路几何大量为空；
- Blocker：机动车路网和步行路网筛选规则失效；
- Blocker：坐标系统错误导致长度或面积计算失真；
- Warning：道路名称缺失比例较高；
- Warning：`service` 道路占比偏高；
- Warning：OSM 与天地图视觉上存在轻微偏移；
- Info：鼓浪屿是独立网络子图；
- Info：边界处存在无道路网格。

## 8. D5 审计输出指标

D5 建议后续 Pipeline 或人工审计输出：

```text
boundary_area_km2
road_raw_count
road_cleaned_count
road_name_missing_ratio
highway_type_distribution
motor_road_count
walk_road_count
service_road_ratio
private_or_restricted_count
motor_component_count
walk_component_count
gulangyu_road_count
grid_count
boundary_grid_count
empty_grid_count
crs_source
crs_analysis
crs_storage
basemap_provider
```

这些指标将写入数据审计文档，并作为 D6/D7 开发 Pipeline 和数据库迁移时的验收依据。

## 9. D5 结论

D5 明确本项目采用可复现边界来源、OSM 路网快照、天地图优先底图、OSM/离线底图兜底、双路网筛选、`EPSG:32650` 米制计算和分级数据质量审计。该方案与 D1-D4 保持一致，能够支撑后续 Pipeline 开发、PostGIS 入库、指标计算和成果解释。
