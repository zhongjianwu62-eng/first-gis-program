# D4 API 契约草案

## 厦门市思明区城市路网结构与可步行性分析平台

| 项目属性 | 内容 |
|---|---|
| 文档版本 | 1.0 |
| 日期 | 2026-06-25 |
| API 前缀 | `/api/v1` |
| 接口类型 | 匿名只读查询 |
| 状态 | 草案，供 D6/D7 实现时细化 |

## 1. API 设计原则

1. 所有业务接口只读；
2. 道路和网格地图数据必须支持 bbox；
3. 地图几何返回 GeoJSON；
4. 统计、详情、说明返回 JSON；
5. 所有结果绑定当前数据版本；
6. 所有错误返回统一结构；
7. 搜索无结果和 bbox 无数据不是系统错误；
8. API 字段可在实现阶段微调，但不得破坏核心语义。

## 2. 系统健康检查

### `GET /health`

用于检查后端服务是否可用。

返回示例：

```json
{
  "status": "ok",
  "service": "siming-walkability-api",
  "timestamp": "2026-06-25T10:30:00+08:00"
}
```

## 3. 系统元信息

### `GET /api/v1/meta`

用于前端初始化时获取系统基本信息。

返回示例：

```json
{
  "project_name": "厦门市思明区路网结构与可步行性分析平台",
  "study_area": "福建省厦门市思明区",
  "data_version": "siming-osm-2026-06-v1",
  "coordinate_system": "EPSG:4326",
  "updated_at": "2026-06-25T10:30:00+08:00",
  "available_basemaps": ["tianditu", "osm", "offline"],
  "default_indicator": "walkability_score"
}
```

## 4. 指标定义接口

### `GET /api/v1/indicators`

用于获取所有指标定义。

返回示例：

```json
{
  "data_version": "siming-osm-2026-06-v1",
  "indicators": [
    {
      "code": "walkability_score",
      "name": "综合可步行性分数",
      "unit": "score",
      "direction": "positive",
      "weight": 1.0,
      "description": "基于路网结构指标计算的综合评价结果。",
      "is_composite": true,
      "display_order": 1
    }
  ]
}
```

字段说明：

| 字段 | 含义 |
|---|---|
| `code` | 指标编码 |
| `name` | 中文名称 |
| `unit` | 单位 |
| `direction` | 正向或反向 |
| `weight` | 权重 |
| `description` | 指标解释 |
| `is_composite` | 是否综合指标 |
| `display_order` | 展示顺序 |

## 5. 网格地图查询

### `GET /api/v1/grids`

用于按当前地图视野查询 500 米网格。

请求参数：

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `bbox` | 是 | `118.05,24.42,118.18,24.52` | 当前地图范围，顺序为 minLng,minLat,maxLng,maxLat |
| `indicator` | 否 | `walkability_score` | 当前设色指标 |
| `classification` | 否 | `quantile` | 分级方式 |
| `limit` | 否 | `5000` | 最大返回数量 |

返回格式：GeoJSON FeatureCollection。

返回示例：

```json
{
  "type": "FeatureCollection",
  "data_version": "siming-osm-2026-06-v1",
  "features": [
    {
      "type": "Feature",
      "id": "grid_001",
      "geometry": {
        "type": "Polygon",
        "coordinates": []
      },
      "properties": {
        "grid_id": "grid_001",
        "walkability_score": 82.5,
        "rank_percentile": 91.2,
        "class_level": 5
      }
    }
  ]
}
```

## 6. 网格详情查询

### `GET /api/v1/grids/{grid_id}`

用于点击网格后获取详细解释。

返回示例：

```json
{
  "grid_id": "grid_001",
  "data_version": "siming-osm-2026-06-v1",
  "summary": {
    "walkability_score": 82.5,
    "rank_percentile": 91.2,
    "class_level": 5,
    "interpretation": "该网格路网密度和交叉口密度较高，整体可步行性潜力较好。"
  },
  "indicators": [
    {
      "code": "intersection_density",
      "name": "交叉口密度",
      "raw_value": 42.1,
      "normalized_value": 0.87,
      "unit": "个/平方公里",
      "district_average": 31.4,
      "direction": "positive"
    }
  ],
  "charts": {
    "radar": [],
    "bar_compare": []
  }
}
```

## 7. 道路地图查询

### `GET /api/v1/roads`

用于按地图视野查询道路。

请求参数：

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `bbox` | 是 | `118.05,24.42,118.18,24.52` | 当前地图范围 |
| `network` | 否 | `walk` | `motor` 或 `walk` |
| `road_class` | 否 | `primary` | 道路等级 |
| `limit` | 否 | `10000` | 最大返回数量 |

返回格式：GeoJSON FeatureCollection。

返回示例：

```json
{
  "type": "FeatureCollection",
  "data_version": "siming-osm-2026-06-v1",
  "features": [
    {
      "type": "Feature",
      "id": "road_001",
      "geometry": {
        "type": "LineString",
        "coordinates": []
      },
      "properties": {
        "road_id": "road_001",
        "name": "厦禾路",
        "road_class": "primary",
        "length_m": 1280.5,
        "network": "motor"
      }
    }
  ]
}
```

## 8. 道路详情查询

### `GET /api/v1/roads/{road_id}`

用于点击道路后获取详情。

返回示例：

```json
{
  "road_id": "road_001",
  "data_version": "siming-osm-2026-06-v1",
  "name": "厦禾路",
  "road_class": "primary",
  "length_m": 1280.5,
  "network_flags": {
    "motor": true,
    "walk": true
  },
  "indicators": {
    "betweenness_centrality": 0.74,
    "degree_related_score": 0.62
  }
}
```

## 9. 道路搜索

### `GET /api/v1/roads/search`

用于道路名称模糊搜索。

请求参数：

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `keyword` | 是 | `厦禾` | 道路名称关键词 |
| `limit` | 否 | `10` | 最大返回数量 |

返回示例：

```json
{
  "keyword": "厦禾",
  "data_version": "siming-osm-2026-06-v1",
  "results": [
    {
      "road_id": "road_001",
      "name": "厦禾路",
      "road_class": "primary",
      "center": [118.11, 24.47],
      "match_score": 0.98
    }
  ]
}
```

无搜索结果时返回空数组，不作为系统错误。

## 10. 全区概览统计

### `GET /api/v1/statistics/overview`

用于加载右侧默认概览。

返回示例：

```json
{
  "data_version": "siming-osm-2026-06-v1",
  "summary": {
    "grid_count": 258,
    "road_count": 1240,
    "total_road_length_km": 532.7,
    "average_walkability_score": 68.4
  },
  "indicator_distribution": [
    {
      "indicator": "walkability_score",
      "bins": [
        { "range": "0-20", "count": 5 },
        { "range": "20-40", "count": 32 }
      ]
    }
  ]
}
```

## 11. 网格排行榜

### `GET /api/v1/rankings/grids`

用于高值和低值网格榜单。

请求参数：

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `indicator` | 否 | `walkability_score` | 排名指标 |
| `order` | 否 | `desc` | `desc` 高值，`asc` 低值 |
| `limit` | 否 | `10` | 返回数量 |
| `bbox` | 否 | `118.05,24.42,118.18,24.52` | 可选地图范围 |

返回示例：

```json
{
  "data_version": "siming-osm-2026-06-v1",
  "indicator": "walkability_score",
  "order": "desc",
  "items": [
    {
      "grid_id": "grid_001",
      "score": 82.5,
      "rank_percentile": 91.2,
      "center": [118.11, 24.47]
    }
  ]
}
```

## 12. CSV 导出

### `GET /api/v1/export/grids.csv`

用于导出当前筛选结果。

请求参数：

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| `indicator` | 否 | `walkability_score` | 当前指标 |
| `bbox` | 否 | `118.05,24.42,118.18,24.52` | 当前地图范围 |
| `classification` | 否 | `quantile` | 分级方式 |

导出字段建议包括：

```text
grid_id
center_lng
center_lat
walkability_score
rank_percentile
class_level
intersection_density
road_density
connectivity_score
data_version
exported_at
```

导出文件名建议：

```text
siming_walkability_grids_2026-06-25.csv
```

## 13. 统一错误结构

所有错误统一返回：

```json
{
  "error_code": "INVALID_BBOX",
  "message": "地图范围参数不正确，请重新调整地图范围。",
  "request_id": "req_20260625_xxxx"
}
```

常见错误码：

| HTTP 状态 | 错误码 | 场景 |
|---|---|---|
| 400 | `INVALID_BBOX` | bbox 格式错误 |
| 400 | `INVALID_INDICATOR` | 指标编码不存在 |
| 400 | `INVALID_NETWORK` | 路网类型错误 |
| 404 | `GRID_NOT_FOUND` | 网格不存在 |
| 404 | `ROAD_NOT_FOUND` | 道路不存在 |
| 413 | `QUERY_TOO_LARGE` | 查询范围或返回量过大 |
| 500 | `INTERNAL_ERROR` | 服务内部错误 |
| 503 | `DATA_VERSION_UNAVAILABLE` | 当前数据版本不可用 |

错误处理原则：

1. 搜索无结果不是错误，返回空数组；
2. 当前 bbox 没有数据不是错误，返回空 GeoJSON；
3. 参数格式错误返回 400；
4. 不存在的网格或道路返回 404；
5. 查询范围太大返回 413；
6. 服务异常返回 500；
7. 当前数据版本不可用返回 503。

## 14. D4 API 契约结论

API 采用 `/api/v1` 版本化只读接口，围绕 meta、indicators、grids、roads、statistics、rankings 和 export 建立契约。地图几何查询返回 GeoJSON，统计、详情和说明返回 JSON。网格和道路地图查询必须支持 bbox，详情接口按 ID 查询，搜索无结果返回空数组。所有正式结果绑定当前数据版本，所有错误响应采用统一 `error_code`、用户可读 `message` 和 `request_id`。

该契约作为前后端开发和测试的初始基线，后续实现可在不破坏核心语义的前提下微调字段。
