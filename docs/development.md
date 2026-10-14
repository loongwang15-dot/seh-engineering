# 开发与检查

Python 要求 3.10+；辅助检查器仍只依赖标准库。本地安装与恢复工具另需 PowerShell 7。

```text
python packages/ai-skill-engineering-hub/scripts/seh_checks.py inspect packages/ai-skill-engineering-hub
python -m unittest discover -s packages/ai-skill-engineering-hub/tests -p "test_*.py" -v
python -m unittest discover -s tests -p "test_installation.py" -v
python -m pytest tests -q
```

Skill 辅助工具目前 39 项 unittest，包括原 28 项和新增 11 项边界/对照测试。安装恢复有 7 项真实 PowerShell 隔离测试；Python 软件保留 11 项原测试。CI 在 Ubuntu 和 Windows 运行 pytest、辅助工具及当前源结构检查。没有 PowerShell 的环境会明确跳过恢复测试，不能把跳过计为通过。

缺少 pytest 时，可直接执行现有零参数软件测试函数，但要明确这种有限执行方式。安装与检查器的 unittest 不需要 pytest。可用 `SEH_POWERSHELL` 指定 PowerShell 7 可执行路径；缺少它时不宣称安装恢复已验证。

修改后更新版本、差异及实际证据；候选 ZIP 与指定源逐文件、逐哈希一致。v3.0.0 [审核报告](../reports/seh/v3.0.0/audit/SEH系统审核报告.md)保留当时结论；v3.0.1 [修复报告](../reports/seh/v3.0.1/README.md)记录新结果，不覆盖旧记录。

历史 PASS 不自动适用于改变后的源。CI 不安装目标应用，不认证完整模型行为。当前安装入口见[本地安装与恢复](deployment/local_installation.md)。
