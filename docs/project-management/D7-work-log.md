# D7 工作记录：本地运行验证

日期：2026-07-01
分支：`docs/d7-local-run-validation`

## 当日目标

在 D6 工程骨架基础上完成本地运行验证，让项目前端和后端第一次真实启动，并记录依赖安装、构建、接口验证和本地预览状态。

## 已完成内容

1. 从本地 D6 提交创建 D7 分支；
2. 安装前端 npm 依赖；
3. 生成 `frontend/package-lock.json`，用于固定前端依赖版本；
4. 运行前端类型检查；
5. 运行前端生产构建；
6. 启动 Vite 前端开发服务器；
7. 验证前端首页返回 HTTP 200；
8. 创建后端 Python 虚拟环境；
9. 安装后端 FastAPI 依赖；
10. 启动 FastAPI 后端服务；
11. 验证 `/health` 接口；
12. 验证 `/api/v1/meta` 接口；
13. 将 Python 可编辑安装生成目录加入 `.gitignore`；
14. 记录 D7 运行验证审计报告。

## 验证结果

| 检查项 | 结果 | 说明 |
|---|---|---|
| 前端依赖安装 | 通过 | `npm.cmd install` 成功，0 个漏洞 |
| 前端类型检查 | 通过 | `npm.cmd run typecheck` 成功 |
| 前端构建 | 通过 | `npm.cmd run build` 成功 |
| 前端本地预览 | 通过 | `http://127.0.0.1:5173/` 返回 HTTP 200 |
| 后端依赖安装 | 通过 | `.venv\\Scripts\\python.exe -m pip install -e .` 成功 |
| 后端服务启动 | 通过 | Uvicorn 启动于 `http://127.0.0.1:8000` |
| 后端健康检查 | 通过 | `/health` 返回 `status=ok` |
| 后端元信息接口 | 通过 | `/api/v1/meta` 返回项目元信息 |

## 发现的问题与处理

| 问题 | 等级 | 处理 |
|---|---|---|
| PowerShell 阻止 `npm.ps1` | Warning | 改用 `npm.cmd` 执行 npm 命令 |
| 前端构建在沙盒内读取配置被拒 | Warning | 授权重跑构建后通过 |
| PowerShell 显示后端中文 JSON 乱码 | Info | 接口可访问，属于终端显示编码问题，后续浏览器/前端处理 UTF-8 |
| Python 可编辑安装生成 egg-info | Info | 已将 `*.egg-info/` 加入 `.gitignore` |
| D6 分支此前未能推送 GitHub | Warning | D7 继续本地验证，后续网络恢复后补推 |

## 当前可访问地址

```text
前端预览：http://127.0.0.1:5173/
后端健康：http://127.0.0.1:8000/health
后端元信息：http://127.0.0.1:8000/api/v1/meta
```

## 审计边界

- D7 不接入真实天地图 token；
- D7 不下载真实 GIS 数据；
- D7 不连接 PostGIS；
- D7 不实现真实地图图层；
- D7 仅验证工程骨架可安装、可构建、可启动、可访问。

## 下一步

D8 建议开始“前后端联通与开发体验完善”，让前端通过 `VITE_API_BASE_URL` 调用后端 `/api/v1/meta`，并在页面上展示后端返回的数据。
