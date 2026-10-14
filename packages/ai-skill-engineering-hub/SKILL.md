---
name: ai-skill-engineering-hub
description: 在用户要求创建、修改、恢复、审计、拆分、合并、迁移、部署或废弃 Skill 时，管理能力来源、需求变更、验证证据和版本恢复。普通设计生产和泛泛讨论不启动工程流程。
---

# AI Skill 工程中枢（Skill Engineering Hub，SEH）v3.0.1

SEH 为可复用 Skill 提供工程治理：明确能力边界，保留来源与用户约束，按任务风险验证，交付可追踪、可恢复的版本。实际生产由相应专业 Skill 执行。本包是指令与离线检查工具；目标应用的发现、路由和调用仍由宿主提供。

## 1. 选择任务模式

先识别用户要求和可用文件。只读取当前模式需要的参考章节；不要把审计、简单修订或一般讨论升级成完整发布。

| 模式 | 目标 | 读取 |
| --- | --- | --- |
| CREATE | 建立新能力或将明确需求标准化为 Skill | [编写与恢复](references/modes-authoring.md#create) |
| UPDATE | 完善或修改既有 Skill，包括结构标准化 | [编写与恢复](references/modes-authoring.md#update) |
| RECOVER | 从现有源和版本恢复能力 | [编写与恢复](references/modes-authoring.md#recover) |
| SPLIT / MERGE | 拆分或整合既有能力 | [重构与迁移](references/modes-refactor.md) |
| MIGRATE | 为指定平台建立适配版 | [重构与迁移](references/modes-refactor.md#migrate) |
| AUDIT | 评估质量、完整性或必要性，保持只读 | [审计与生命周期](references/modes-lifecycle.md#audit) |
| DEPLOY | 安装或发布已准备好的版本 | [审计与生命周期](references/modes-lifecycle.md#deploy) |
| DEPRECATE | 废弃、替换或归档版本 | [审计与生命周期](references/modes-lifecycle.md#deprecate) |

混合请求按依赖顺序处理，例如 UPDATE → 验证 → DEPLOY。修改授权不自动扩展为外部发布授权；已有授权可直接沿用。不得自动创建新聊天、向他人发送消息或接管其他 Skill。任务范围变化就在当前任务记录和重新规划，遵循宿主关于聊天管理的规则。

## 2. 选择流程强度

- **LIGHT**：单一 Skill 的简单创建、局部修订或有限审计；没有复杂依赖、平台变更或既有行为合同变化。记录目标、来源、差异及必要验证即可；可在答复中记录，不要求建立空目录、独立状态文件或完整台账。
- **FULL**：改变既有触发/边界/行为/关键约束、重构、恢复、迁移、部署、多 Skill 协作，或用户要求系统性优化。建立[需求与变更记录](references/requirement-ledger.md)、适用能力映射和验收；修改或安装已有版本时保存快照，纯审计不要求生成映射或备份被审文件。
- RECOVER、SPLIT、MERGE、MIGRATE、DEPLOY 使用 FULL；记录门拒绝这些模式的 LIGHT 标签，不能借标签跳过回归。其他模式仍按实际影响选择强度。
- 无法判断影响时先盘点并分析；只有实质性缺失才请求输入。不要把格式修订自动判为重大变更。LIGHT 发现更大影响时升级 FULL 并说明原因。

两种流程都必须保留用户意图、处理真实依赖、验证交付和如实说明未验证项。24 项工程模块是适用性检查框架，详见[治理规则](references/governance.md)；不要求每个 Skill 拥有 24 个章节或相同目录。

## 3. 统一执行入口

1. **盘点**：确认模式、强度、源文件/版本、目标及权限，区分可读取的事实与文档声明。缺输入时继续不依赖它的工作。
2. **建立基线**：从用户请求和现有能力提取适用要求，标明来源及授权依据。明确的请求本身可作为确认依据，不另设例行确认关卡。
3. **识别 Canonical**：优先使用有来源和版本证据的完整源。安装版可在证据支持时被登记为 Canonical；不存在独立源并不否定它。多份冲突时比较来源、日期和内容，不单凭最大版本号决定。
4. **执行当前模式**：AUDIT 只读目标，输出发现；CREATE 建立源；其他修改先保存可恢复版本。只在迁移/部署或多版本同步时生成 Adapter，不为单平台任务制造额外副本。
5. **验证**：按[验收规则](references/acceptance-matrix.md)执行必要用例。通过文件检查不能推断模型行为或平台运行通过；重排文字后的语义保真需要人工或模型核对。
6. **交付并停止**：报告完成范围、变更、证据、限制、版本和恢复方法；已满足请求就结束。涉及实际安装时，再核对目标文件并执行目标可运行的检查。

## 4. 规则、冲突与变更

宿主指令与用户明确要求优先；本 Skill 的内部治理规则不凌驾于它们。Canonical 记录既有能力，用户授权的变更通过 CR 更新它；适配器只转换平台表达，不能暗改能力。

本入口及当前模式合同共同定义 v3.0.1。历史规范仅作为恢复证据，不作为第二套执行指令。冲突处理顺序统一为：识别 → 分析影响 → 应用明确优先级或已有授权 → 执行并留痕。

- 只阻断受影响阶段。无关冲突记入待办，不停止其他工作。
- 涉及真实歧义、关键缺失或权限不足，明确需要什么及原因；不可虚构来源、测试或批准。
- 用户修改需求时更新影响分析与基线，继续已授权工作；只有用户要求暂停才使用 PAUSED。Workflow Lock 保护必要依赖顺序，不冻结用户意图。
- 发现失败先分类并定向修正。默认最多 3 次修正重试；每次有不同修正动作并重新验证。权限拒绝或无可用输入不属于可盲目重试的错误。

## 5. 状态与证据

Stage 表示正在进行的工作；State 表示能否推进；QA 状态表示已验证什么。三者分别记录，避免把审计发现问题等同于审计任务未完成。

| State | 进入条件与恢复方式 |
| --- | --- |
| PROCESSING | 执行本模式的盘点、修改、审计或验证。LIGHT 可只用普通进度说明。 |
| WAITING_INPUT | 缺少影响下一步的必需输入；说明缺项，继续独立工作，获得输入后复核基线。 |
| NEEDS_REVISION | 已定位可修正失败；记录原因、修正与重试计数，修正后重新验证。 |
| BLOCKED / ERROR | 受影响阶段无法推进，或工具异常；保存有效产物并说明恢复入口。 |
| PAUSED / CANCELLED | 用户明确暂停或取消；恢复时检查源版本、基线和待执行动作。 |
| COMPLETED | 当前请求产物和必要检查已完成。审计可完成并报告被审对象仍 BLOCKED/UNVERIFIED。 |

FULL 记录 Task ID、模式/强度、Skill ID/Version、Baseline/CR、Stage/State、最近通过的检查、有效产物、失败与下一步。源文件变动后只重跑受影响检查，不照搬旧 PASS；跨会话恢复先核对版本与哈希。详细记录见[治理规则](references/governance.md)。

## 6. 工具与验证边界

普通指令任务需要可读取的 Skill 源和当前宿主的文件工具。修改需要写权限；部署需要目标访问与授权。可选 Python 3.10+ 标准库工具无需 SEH 软件 v1.0.0 或网络依赖：

```text
python scripts/seh_checks.py inspect <skill-directory>
python scripts/seh_checks.py compare <canonical-directory> <installed-directory>
python scripts/seh_checks.py gate <qa-record.json>
python -m unittest discover -s tests -p "test_*.py"
```

`inspect` 检查本包约定的入口、引用与版本；不是通用 YAML 验证器。`compare` 检查源文件逐字节一致性；平台新增元数据另列，不推断语义等价。`gate` 检查验收记录是否完整及证据文件哈希；不判断证据内容是否证明某个行为。调用方式和记录格式见[验收规则](references/acceptance-matrix.md)。工具不可用时可人工核对并说明覆盖边界；不安装无关依赖。

## 7. 交付报告

LIGHT 简述结果、实际验证和限制。FULL 报告：模式与强度、Canonical 来源/版本、基线要求数与已覆盖数、授权变更与缺失、结构/功能/回归/保真/部署的结果和证据、阻塞原因、目标环境、版本及恢复点。

- 每项使用 PASS / FAIL / UNVERIFIED / N/A；N/A 必须有适用性理由。
- **PASS** 只针对全部适用检查有证据的明确范围；FAIL 导致该范围 BLOCKED，缺必要证据则 UNVERIFIED。
- 分开写 task_result、package_qa、behavior_qa、deployment_qa。离线交付任务完成后，尚未请求的部署可为 N/A；目标应用真实行为仍可 UNVERIFIED。
- 发布资格受必要运行门约束；未验证版本可以作为候选交付，不能自称已具备完整生产能力。
- 维护依据真实失败和效果数据；记录遗漏、返工、执行成本和恢复结果，只有改善证据才扩充规则。

当前版本、兼容性和已知限制见[版本记录](references/version-history.md)。
