# 开发与检查

在仓库根目录运行，Python 要求 3.10+。中文路径环境建议设置 `PYTHONUTF8=1`。

```text
python packages/ai-skill-engineering-hub/scripts/seh_checks.py inspect packages/ai-skill-engineering-hub
python -m unittest discover -s packages/ai-skill-engineering-hub/tests -p "test_*.py" -v
python -m pip install pytest
python -m pytest tests -q
```

辅助工具测试目前 28 项，软件测试目前 11 项。`tests/conftest.py` 为各 `packages/seh-*` 模块设置导入路径；无需为了运行这些测试移动软件模块。CI 使用相同检查，不安装目标应用，不验证全部 Skill 行为。

缺少 pytest 时，可直接执行现有零参数软件测试函数，但须在报告中说明这种有限执行方式。不要把依赖缺失写为测试通过。

修改 Skill 后更新包内版本、变更记录和必要证据；仅整理仓库文档不升级 Skill 版本。下载包应与指定源版本逐文件、逐哈希一致。现有审核反例见[审核报告](../reports/seh/v3.0.0/audit/SEH系统审核报告.md)，原始输入和命令输出保留在本地；不能由现有正向测试通过推断这些已知问题已修复。

`reports/` 是保存的历史验证记录。记录中的旧执行路径和命令属于当时环境，不能作为可以在任意机器直接运行的安装脚本；新检查须读取当前源重新产生结果。
