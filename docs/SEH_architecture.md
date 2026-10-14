# SEH 架构与实现边界

当前仓库有两条独立实现线：

| 实现 | 位置 | 负责什么 |
| --- | --- | --- |
| SEH Skill 3.0.1 | `packages/ai-skill-engineering-hub/` | 提供九模式工程合同；宿主 Agent 执行文件操作、专业生产和平台调用 |
| SEH Python 软件 1.0.0 | `packages/seh-*/` | 基础数据对象、包结构检查、注册表和工程管理等原型模块 |

Skill 的 `references/` 按当前任务读取；`scripts/seh_checks.py` 使用 Python 标准库做结构、复制一致性与证据记录检查。该工具不负责自动发现、模型路由、语义认证、状态持久化或平台部署。

软件的包检查器仍采用旧固定目录合同；旧模板位于 `templates/legacy-skill/`。注册表 `registry/registry.json` 是原型数据，当前为空，不代表本机已安装 Skill 的实时清单。

发布文件来自 Canonical Skill 源包；报告记录验证范围，归档保存旧源。源码、下载包、安装版及目标应用运行需要分别验证。当前质量状态见[已知问题](known-issues.md)和[审核报告](../reports/seh/v3.0.0/audit/SEH系统审核报告.md)。

当前修复证据见[v3.0.1 报告](../reports/seh/v3.0.1/README.md)；上述 v3.0.0 审核保留当时的发现。仓库 tools/ 的 PowerShell 安装器是独立附件，不改变 Skill 的 Python 标准库依赖。
