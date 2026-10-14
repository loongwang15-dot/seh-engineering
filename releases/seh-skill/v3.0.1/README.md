# SEH Skill 3.0.1 验证候选

下载：[ai-skill-engineering-hub-v3.0.1.zip](ai-skill-engineering-hub-v3.0.1.zip)。当前[Canonical](../../../packages/ai-skill-engineering-hub/README.md)、[逐文件清单](package-manifest.json)、[修复与验证](../../../reports/seh/v3.0.1/README.md)。

ZIP 含 ai-skill-engineering-hub/ 下的完整 14 文件；逐项回读与当前源 SHA-256 一致。已修复 F-01 至 F-04，39 项检查器测试保留原 28 项并补充边界回归。

F-05 的本地安装与恢复由仓库 tools/ 单独提供，经 7 项隔离恢复测试；它们不是网页版依赖。[本地安装](../../../docs/deployment/local_installation.md)需要明确目标、备份、恢复记录及文件权限。

状态保持 unverified：下载包一致和测试通过不能代替所有目标应用的完整运行认证。旧 [v3.0.0 候选](../v3.0.0/README.md)原样保留。
