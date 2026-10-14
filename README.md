# Skill Engineering Hub（SEH）

SEH 帮助管理可复用 AI Skill 的创建、变更、审计、迁移、发布与恢复。本仓库包含可以交给 Agent 使用的 **SEH Skill**，以及独立的 **SEH Python 软件原型**。

| 内容 | 当前版本 | 入口与状态 |
| --- | --- | --- |
| SEH Skill | 3.0.1 | [SKILL.md](packages/ai-skill-engineering-hub/SKILL.md)；验证候选，`unverified` |
| Python 软件 | 1.0.0 | [pyproject.toml](pyproject.toml)；基础库与固定目录检查器原型 |

两条版本线分别维护。Skill 不需要先安装软件；软件的旧目录检查器也不能作为 v3.0.1 Skill 的质量认证。

## 从这里开始

- **使用 Skill**：[源包说明](packages/ai-skill-engineering-hub/README.md)、[九种任务模式](packages/ai-skill-engineering-hub/SKILL.md)、[候选下载包](releases/seh-skill/v3.0.1/README.md)。
- **查看质量**：[当前已知问题](docs/known-issues.md)、[v3.0.1 修复验证](reports/seh/v3.0.1/README.md)、[系统审核](reports/seh/v3.0.0/audit/SEH系统审核报告.md)、[优化验收与证据](reports/seh/v3.0.0/README.md)。
- **开发维护**：[检查方法](docs/development.md)、[文档索引](docs/README.md)、[目录规则](docs/repository-layout.md)、[版本变化](CHANGELOG.md)。
- **恢复历史**：[归档索引](archives/README.md)、[v2.4 源包快照](archives/seh-skill/v2.4-before-20261013/ai-skill-engineering-hub/SKILL.md)。

## 仓库结构

```text
packages/       SEH Skill 源包和 seh-* Python 模块
docs/           使用、开发、目录规则及旧软件规范
tools/          可恢复本地安装/回滚工具，PowerShell 7
tests/          软件与安装恢复测试
templates/      旧固定目录模板，保留兼容用途
registry/       软件原型的注册表数据
reports/        验收、审核和文件保留记录
releases/       有版本的 Skill 候选下载包
archives/       可恢复的历史源与既有归档
.github/        基础自动检查
```

本地 `delivery/`、安装器、独立仓库和其他设计项目已忽略，原文件保留在原处。公开仓库只纳入 SEH 相关内容，目录迁移与保留记录见[整理说明](docs/repository-layout.md)。

## 当前验证边界

v3.0.1 保留原 28 项并通过全部 39 项辅助工具测试；软件保留 11 项基础测试，安装器新增 7 项隔离恢复测试。原 6 个检查器反例已按正确预期验证。历史 12 个工程请求与 CLI 单例不自动扩展为新版完整认证；全量旧模型行为回归、完整目标应用运行和长期收益仍未完全验证。

v3.0.0 的候选 ZIP 和原始审核结论保持不变。v3.0.1 修复 F-01 至 F-04，当前 tools/ 安装器处理 F-05；详细结果见修复报告。辅助工具 PASS 不能单独证明完整生产资格。
