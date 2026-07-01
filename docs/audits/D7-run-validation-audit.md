# D7 本地运行验证审计报告

日期：2026-07-01
审计分支：`docs/d7-local-run-validation`

## 审计范围

- `frontend/`
- `backend/`
- `.gitignore`
- `docs/project-management/D7-work-log.md`
- `docs/audits/D7-run-validation-audit.md`

## 审计结果

| 检查项 | 结果 | 说明 |
|---|---|---|
| 前端依赖安装 | 通过 | npm 安装成功，生成依赖锁文件 |
| 前端安全审计 | 通过 | npm install 输出 0 个漏洞 |
| 前端类型检查 | 通过 | Vue TypeScript 检查通过 |
| 前端构建 | 通过 | Vite 生产构建成功 |
| 前端本地预览 | 通过 | `http://127.0.0.1:5173/` 返回 HTTP 200 |
| 后端依赖安装 | 通过 | FastAPI、Uvicorn、Pydantic 等依赖安装成功 |
| 后端服务启动 | 通过 | Uvicorn 本地启动成功 |
| `/health` 接口 | 通过 | 返回 `status=ok` |
| `/api/v1/meta` 接口 | 通过 | 返回项目元信息 |
| 本地产物隔离 | 通过 | `node_modules`、`dist`、`.venv` 均被忽略 |
| Python egg-info 隔离 | 通过 | 已将 `*.egg-info/` 加入 `.gitignore` |
| 凭证安全 | 通过 | 未发现真实天地图 token 或真实连接凭证 |
| 数据安全 | 通过 | 未下载或提交真实 GIS 数据 |

## 验证命令摘要

```text
npm.cmd install
npm.cmd run typecheck
npm.cmd run build
npm.cmd run dev -- --host 127.0.0.1
.venv\\Scripts\\python.exe -m pip install -e .
.venv\\Scripts\\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 风险记录

| 风险 | 等级 | 说明 |
|---|---|---|
| GitHub 推送网络不稳定 | Warning | 此前 D6 推送多次被连接重置，D7 提交后需要继续重试 |
| PowerShell npm 脚本策略 | Warning | 使用 `npm.cmd` 作为 Windows 下的稳定执行方式 |
| Docker 尚未验证 | Info | D7 聚焦前后端本地运行，PostGIS 容器留到后续验证 |
| 后端中文输出在 PowerShell 中乱码 | Info | 接口可访问，后续通过浏览器或前端统一验证 UTF-8 展示 |

## 审计结论

D7 已完成本地运行验证。前端可以安装、类型检查、构建并启动预览；后端可以安装依赖、启动服务并返回健康检查与元信息接口。项目已经从工程骨架阶段进入“可本地运行”的代码阶段。

D7 可作为 D8 前后端联调和开发体验完善的输入。
