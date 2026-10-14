# AI Skill工程中枢（SEH Skill）

此目录是 SEH Skill v3.0.0 的 Canonical 源包。入口为 `SKILL.md`；九种任务模式和治理细节在按需读取的 `references/` 中。修改当前源不等于任何安装版已同步。`VERSION` 是 Skill 版本；仓库根版本属于独立的 SEH 软件工程。

指令工作流使用宿主的文件工具；可选 `scripts/seh_checks.py` 只依赖 Python 3.10+ 标准库，提供结构、复制完整性和 QA 证据记录检查。运行 `python -m unittest discover -s tests -p "test_*.py"` 验证辅助工具。工具不负责自动路由、生成内容、持久状态或平台安装。

当前发布状态仍为 `unverified`，因为特定目标应用的自动发现和完整运行须分别验证。实际测试以项目验收记录为准，不把本文件声明或包存在当成功证据。v3.0.0 将固定 24 项结构改为按任务适用检查；不再使用 legacy 占位目录。本包不兼容 SEH 软件 v1.0.0 的固定目录检查，但不需要该软件才能执行。
