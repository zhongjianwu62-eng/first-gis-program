# D6 工作记录：工程骨架搭建

日期：2026-06-27
分支：`docs/d6-project-scaffold`

## 当日目标

从 D1-D5 的文档与数据方案进入真实工程阶段，建立前端、后端、Pipeline、数据库、部署和测试的轻量工程骨架。

## 已确认决策

| 决策项 | 结果 |
|---|---|
| D6 路线 | A：稳健骨架优先 |
| 前端 | Vue 3 + TypeScript + Vite 工作台壳子 |
| 后端 | FastAPI 最小服务 |
| 后端接口 | `/health`、`/api/v1/meta` |
| Pipeline | 只建目录和说明，不下载真实数据 |
| Database | 只建目录和说明，不创建正式表迁移 |
| Deploy | 开发版 Docker Compose，先提供 PostGIS 服务 |
| 凭证管理 | `.env.example` 提供空变量，真实天地图 token 不入库 |
| Git 基线 | D6 接在 D5 分支之后，等待 D5 合并后可继续 rebase 或创建 PR |

## 完成内容

1. 建立 `frontend` 工程骨架；
2. 建立 Vue 3 工作台占位页面；
3. 建立 `backend` FastAPI 工程骨架；
4. 实现 `/health` 接口；
5. 实现 `/api/v1/meta` 接口；
6. 建立 `pipeline` 目录和说明；
7. 建立 `database` 目录和说明；
8. 建立 `deploy/docker-compose.yml`，提供 PostGIS 服务；
9. 建立根目录 `.env.example`；
10. 建立根目录 `README.md`；
11. 建立跨模块 `tests` 目录说明；
12. 建立 D6 工程骨架审计报告。

## 审计重点

- 不提交真实 `.env`；
- 不提交真实天地图 token；
- 不下载或提交真实 GIS 数据；
- 不提交课程压缩包或原始实验数据；
- D6 不超范围实现真实地图、PostGIS 查询或 Pipeline 下载；
- 前端、后端、Pipeline、database、deploy、tests 目录与 D4 保持一致。

## 遗留事项

- 等 D5 合并到 main 后，D6 分支需要核对基线；
- D7 需要安装依赖并验证前端和后端可启动；
- D7 需要根据实际环境处理 Docker 配置权限警告；
- 后续需要补充 GitHub Actions、lint、测试和格式检查。

## D6 结论

D6 已建立轻量工程骨架，使项目从文档阶段进入可开发工程阶段。该骨架不包含真实业务数据和真实凭证，可作为 D7 开发环境验证与基础运行测试的输入。
