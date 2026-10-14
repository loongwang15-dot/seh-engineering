# SEH 验收与证据

## 选择检查

验收围绕本次变化和用户请求选取；没有执行的用例不能写 PASS。LIGHT 格式修订核对差异与链接即可；FULL 行为变更执行正常、缺输入、边界和受影响异常/旧能力。AUDIT 按审计范围报告，不要求为结构审计跑全生命周期。

| 门 | 所需证据与范围 |
| --- | --- |
| structure | 入口/frontmatter、可读引用、必要依赖、版本一致性；不能证明决策正确。 |
| fidelity | 关键原能力到新位置的映射、授权变更及语义核对；同内容复制可辅以哈希。新建无历史源时可 N/A，但用户输入保留仍须核对。 |
| behavior | 真实请求的输入、实际执行、观察结果、成果及判定依据；显式加载的子代理测试只能证明该宿主的指令行为。 |
| regression | 未改旧能力及变化影响的代表性用例。首次创建、纯结构审计或无行为影响的 LIGHT 修订可 N/A，写明原因。 |
| deployment | 安装授权、旧版恢复点、目标回读、目标新会话发现、正反触发和关键执行。只复制文件不等于此门通过。 |

## 用例判定

| 用例 | 可观察的通过条件 |
| --- | --- |
| 正常/完成 | 所选模式产生请求结果，质量满足当前基线，完成后停止。 |
| 缺输入 | 先查可获得来源；只对不可推导的关键缺项等待，不虚构；继续独立工作。 |
| 边界/反触发 | 普通生产或泛泛讨论不启动完整治理，实际专业能力有明确路由。 |
| 冲突/变更 | 应用已有用户要求及规则优先级；无关冲突不全局停工；未解决关键冲突记录待决。 |
| 失败/重试/恢复 | 保存有效成果，修正针对原因且次数有限；恢复核对版本，不使用过时 PASS。 |
| 保真/拆合 | 旧能力有明确归属，授权变化有记录，没有暗删或把摘要当完整恢复。 |
| 目标运行 | 分别观察文件安装、宿主发现和实际行为，准确标记不可访问项目。 |

记录每例的输入、预期、实际执行与输出、观察结果、判定理由、来源版本/哈希和证据。独立测试不要向执行者透露预期答案或猜测缺陷；允许其读取 Skill 和原始素材。测试产生的样例、模拟记录和离线结果不能充当真实外部应用验证。修改后只重跑受影响例子。

## 标准库工具

从 Skill 根目录运行入口列出的命令。`inspect` 只支持本包使用的标量 frontmatter 和可选 manifest/VERSION 一致性；完整 YAML 语法使用宿主提供的正式检查器。它还检查 Markdown 本地引用与标题锚点，拒绝逃出 Skill 根的本地引用或符号链接。

支持的入口字符串为普通文字标量、单引号字符串和 JSON 兼容的双引号字符串；集合、布尔/数值/null、多行或未支持的 YAML 标记明确拒绝。存在的 VERSION 必须非空。Markdown 依赖包括内联、完整/折叠/简写引用式链接；代码围栏、行内代码、注释和未使用的引用定义不作为文件依赖。

`compare` 逐文件比较完整源，输出缺失、变化和目标新增文件；新增平台文件不自动判失败，需人工确认用途。不要拿不同表达的 Adapter 做逐字节“语义验证”。

`gate` 输入 JSON 记录，stdout 输出结论。exit 0 是声明范围的记录完整且证据哈希有效；1 是 BLOCKED；2 是 UNVERIFIED。它不运行目标应用、不验证证据论证、不自动给 Skill 晋级。

schema_version 必须是整数 1，布尔值和浮点数不能代替它。RECOVER、SPLIT、MERGE、MIGRATE、DEPLOY 的 profile 必须为 FULL；非法组合直接 BLOCKED，不能通过 LIGHT 标签获得回归豁免。

记录字段：schema_version=1、task_id、mode（入口九种之一）、profile（LIGHT/FULL）、scope（PACKAGE/BEHAVIOR/DEPLOYMENT）、checks 数组。每项有唯一 id、status（PASS/FAIL/UNVERIFIED/N/A）、reason，以及 evidence 数组。证据每条为相对于记录目录的 path、实际 sha256、kind（command/file/agent_behavior/target_app/manual）。证据文件必须在记录目录内；子代理结果先保存为文件。PASS 必须有证据；其他状态写原因。N/A 不表示通过。

必需检查 ID 由 scope 决定，不能通过漏填绕过：PACKAGE 至少 structure/fidelity；BEHAVIOR 加 behavior/regression；DEPLOYMENT 再加 deployment。structure、behavior 和 DEPLOYMENT 中的 deployment 不能 N/A；仅 CREATE 的 fidelity、CREATE/AUDIT/LIGHT 的 regression 可有理由地 N/A。deployment 的 PASS 还必须有 target_app 类型证据，仅文件复制记录会降为 UNVERIFIED。结构审计使用 PACKAGE 并在 fidelity 记录现有内容核对，避免强迫审计生成 Adapter。scope 只是本次验收范围，正式生产部署资格使用 DEPLOYMENT；目标行为不能检验时写 UNVERIFIED。

示例（以下不是测试结果）：

```json
{"schema_version": 1, "task_id": "example", "mode": "CREATE", "profile": "LIGHT", "scope": "PACKAGE", "checks": [
  {"id": "structure", "status": "UNVERIFIED", "reason": "尚未执行入口检查", "evidence": []},
  {"id": "fidelity", "status": "N/A", "reason": "首次创建，无历史能力源；用户输入另行核对", "evidence": []}
]}
```

报告始终区分任务完成、文件包 QA、行为 QA、目标部署 QA。适用 FAIL 阻断相关范围；缺必要运行证据为 UNVERIFIED。能交付候选不等于能宣称生产通过。
