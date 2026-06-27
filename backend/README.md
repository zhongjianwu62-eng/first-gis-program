# Backend

FastAPI 后端工程骨架。

D6 当前提供最小只读接口：

```text
GET /health
GET /api/v1/meta
```

## 启动

```text
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```

默认访问：

```text
http://localhost:8000/health
http://localhost:8000/api/v1/meta
```

## 当前边界

D6 不连接 PostGIS，不执行 GIS 查询，不读取真实数据版本。
