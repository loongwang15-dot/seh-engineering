# 文档索引

| 需要了解什么 | 文档 |
| --- | --- |
| 当前系统组成与边界 | [架构](SEH_architecture.md) |
| 如何检查与维护 | [开发与检查](development.md) |
| 文件应该放在哪里 | [目录规则及迁移表](repository-layout.md) |
| 当前版本有哪些缺陷 | [已知问题](known-issues.md) |
| 软件与 Skill 交付格式区别 | [交付说明](handoff.md) |
| 原始软件产品设想 | [产品规范](product.md) |
| 旧软件元数据与固定目录检查 | [Skill 规范](specification/skill_standard.md)、[Manifest 草案](specification/manifest_schema.yaml)、[验证体系](specification/validation_system.md) |
| 旧软件的生命周期与依赖设想 | [生命周期](specification/lifecycle.md)、[依赖管理](specification/dependency_management.md) |
| 旧软件治理及登记设想 | [命名](governance/naming_rules.md)、[质量标准](governance/quality_standard.md)、[注册表](registry.md)、[版本](versioning.md) |
| 原始部署说明 | [GitHub](deployment/github_deployment.md)、[GPT 加载](deployment/gpt_agent_loading.md) |

`specification/`、`governance/`、注册表、产品与部署短文来自软件 v1.0.0 原始规范，部分是设计设想，并不证明对应集成已经实现。它们保留供兼容和历史理解；**当前 SEH Skill 执行合同以包内 [SKILL.md](../packages/ai-skill-engineering-hub/SKILL.md) 及其参考文件为准**。不把旧模板的固定目录要求套到当前 Skill。
