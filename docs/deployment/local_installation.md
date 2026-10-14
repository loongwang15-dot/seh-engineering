# 本地安装与可恢复更新

当前入口是仓库 `tools/install-seh.ps1`、`tools/rollback-seh.ps1` 和共享模块，需 PowerShell 7。它们不属于 14 文件 Skill 包；网页版无需运行它们。旧 `delivery/seh-v3.0.0/` 机器专用附件仅保留为历史证据。

先核对源包、授权与目标旧版。目标和备份路径由调用者明确指定；目录权限不足时使用宿主正常审批。备份与恢复记录必须是新的位置，且位于源与安装目录之外。

```powershell
# 用真实、已授权路径替换参数，不直接执行占位路径。
pwsh -File tools/install-seh.ps1 -Source <canonical-dir> -Target <installed-dir> -Backup <new-backup-dir> -Record <new-plan.json>
pwsh -File tools/rollback-seh.ps1 -Record <plan.json> -Target <the-same-installed-dir> -Backup <the-same-backup-dir>
```

安装先核对路径及现有文件、验证备份，在第一份目标文件替换前原子写入并刷新恢复计划。每次写入先更新计划，再复制到同目录临时文件，核对哈希后替换；部分复制不能截断现有安装文件。错误会标为 INTERRUPTED；使用同一记录启动恢复，不依赖安装走完。

回滚在任何恢复或移除前核对所有相关路径、备份与目标哈希。出现安装后的新内容、删除或备份修改时停止并保留现场；无关文件不移除。恢复同样先暂存再替换，回滚自身中断后可再次运行；已恢复文件不会误删。无法确认归属的临时内容保留并提示。

CopyIntegrity=PASS 只证明文件复制；宿主发现、触发、路由和执行另行验证。机器安装计划及绝对路径保留本地，不提交公开仓库。实测范围见[修复报告](../../reports/seh/v3.0.1/README.md)。
