# 仓库目录与整理记录

整理日期：2026-10-14。用户授权同步 GitHub 并整理 SEH 仓库；本轮只改变仓库组织与说明，SEH Skill 3.0.0 的 14 文件内容保持不变。

## 放置规则

| 目录 | 内容与维护方式 |
| --- | --- |
| `packages/ai-skill-engineering-hub/` | 当前 Skill 唯一 Canonical 源；安装到其他位置需另行比对 |
| `packages/seh-*/` | Python 软件模块，保留导入路径 |
| `docs/` | 项目导航、当前限制及旧软件规范；不放运行输出 |
| `tests/` | 软件与安装恢复测试；Skill 辅助工具测试留在该 Skill 包内 |
| `tools/` | 无机器专用路径的 PowerShell 7 安装/回滚工具 |
| `templates/legacy-skill/` | 旧固定目录示例；新 Skill 不强制采用 |
| `registry/` | 软件原型的数据文件 |
| `reports/seh/<version>/` | 验收、审核、精选原始证据与来源清单 |
| `releases/seh-skill/<version>/` | 指定版本候选 ZIP 与逐文件哈希 |
| `archives/` | 历史完整源、恢复点与既有其他 Skill 历史包 |
| `delivery/` 等本地工作目录 | 已忽略；保留原交付、安装器、其他项目及独立仓库 |

## 本次迁移

| 原位置 | 现位置 |
| --- | --- |
| `PRODUCT.md`、`HANDOFF.md` | `docs/product.md`、`docs/handoff.md` |
| `core/` | `docs/specification/` |
| `governance/`、`deployment/` | `docs/governance/`、`docs/deployment/` |
| `versioning/version_rules.md` | `docs/versioning.md` |
| `registry/registry_rules.md` | `docs/registry.md` |
| `packages/_template_skill/` | `templates/legacy-skill/` |
| 原 IP Design OS 归档 ZIP | `archives/other-skills/` |

23 个移动文件在移动后逐项 SHA-256 相同，清单见[保留记录](../reports/repository-organization-20261014.json)。旧软件架构说明另按当前实际代码重写，其他移动文件保留内容。Git 历史保留旧位置；整理前提交为 `13926504b0f2fcdbf0b8803770fdfd27a23d1fd7`。

优化与审核原始目录仍留在本地 `delivery/seh-v3.0.0/`、`delivery/seh-v3.0.0-audit-20261013/`，避免破坏既有路径、证据哈希和其他任务。公开报告移除了机器绝对路径，并注明它们是脱敏副本；原始哈希、公开文件哈希和未公开内容见[证据索引](../reports/seh/v3.0.0/README.md)。完整原始证据只保留在本地，不公开原始会话事件、安装状态和运行附件。

其他设计包、Apple 演示文件、Docker 安装文件以及 `repository-sync/` 下的独立 Git 仓库保留原位，由明确忽略规则排除。新文件提交前应检查暂存清单，避免把机器配置、原始会话事件或其他项目资产加入 SEH。

同日后续 v3.0.1 修复更新当前 Canonical，新增 tools/、安装恢复测试和新版本报告/候选。以上 v3.0.0 整理记录只描述原同步；14 文件旧原件仍完整保留在 v3.0.0 发布 ZIP 中，不能把“当时未修改”读为当前未修复。
