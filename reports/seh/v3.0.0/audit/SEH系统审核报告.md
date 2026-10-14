> 公开脱敏副本：机器绝对路径已替换为通用标签；正文中的日志和附件名指向本地保留的原始证据。审核结论未修改。

# SEH v3.0.0 系统审核报告

完成日期：2026-10-14（Asia/Shanghai）；Task/Baseline：SEH-AUDIT-20261013（任务跨日，ID保留）；模式 AUDIT / FULL。

用户依据：“用SEH给我系统性的审核一下刚刚新增的这个skill”，随后明确对象“SEH v3.0.0”。本次只读审核源包、安装版和已有证据，执行隔离辅助工具负向检查。没有修改、升级、安装或发布被审Skill。记录及模拟输入仅写入本项目的审核目录。

**结论：核心工程合同较完整，具有实际使用价值；辅助检查器存在可复现的漏检、误判及验收组合校验缺口，当前不能给予完整生产质量认证。** 原28项测试通过的事实仍成立，但不能代表未覆盖条件正确。现有源包本身结构有效；工具处理其他输入的缺陷与当前源文件损坏是两种不同结论。

Canonical：本项目 packages/ai-skill-engineering-hub，v3.0.0。入口SHA-256为70891972f679f0eaff811b92e6757f56db90745f603d5d33a80eac0575b293b5。<installed-skill-alias>是指向<installed-skill-root>的目录联接，两条路径是一份安装。源码与安装版14/14文件一致；审核前后两份文件清单和哈希完全相同。

## 1. 本次基线与覆盖

以下10项是对用户系统审核请求的工程拆解，不冒充用户逐条提出的原话。10/10维度均已给出判断；覆盖不等于通过。

| ID | 维度 | 结论及证据边界 |
| --- | --- | --- |
| AUD-01 | 身份、版本、源与安装一致性 | PASS：入口/manifest/VERSION一致，14/14文件与发布清单和安装版一致 |
| AUD-02 | 触发、排除和职责边界 | PASS（文档及既有代表场景）：工程请求触发，生产/概念讨论不启动完整流程；自动自然语言选择仍未全面测试 |
| AUD-03 | 九模式输入、流程、输出与完成 | 较完整：都有专门合同；既有12个工程请求覆盖各模式，但以简单文本能力为主 |
| AUD-04 | LIGHT/FULL与适用性 | 文档规则合理；工具FAIL：允许不符合入口要求的LIGHT迁移/部署记录跳过回归 |
| AUD-05 | 输入缺口、冲突、状态、重试与恢复 | 核心规则一致，代表场景有执行记录；真实中断后跨会话恢复与复杂故障仍UNVERIFIED |
| AUD-06 | Canonical、CR与能力保真 | 有来源/授权变化和62/62章节处理记录，目标哈希有效；不等于全部语义或旧模型行为回归通过 |
| AUD-07 | 结构检查器正确性 | 当前源包PASS；负向边界FAIL：Markdown引用漏检/误报、空VERSION及非字符串description被接受 |
| AUD-08 | QA记录、证据与发布门 | 证据文件哈希检查有效，语义审查边界写明；组合约束和schema类型存在缺口 |
| AUD-09 | 测试证据与回归可信度 | 原28项测试再次PASS；既有12份观察记录未变；新增12项中7项不符预期；旧完整行为回归维持UNVERIFIED |
| AUD-10 | 部署、维护与必要性 | 本地复制及CLI单次审计有证据；隔离正常回滚通过，中断复制后的配套回滚失败；其他平台/完整目标运行未测；多版本治理有价值，实际收益未量化 |

## 2. 实际检查

- 重新运行现有28项unittest，全部通过；用正式quick_validate重新检查本源包，通过。
- 本源包14处本地引用有效。源码/安装文件、ZIP内容、发布清单全部一致。
- 62个旧章节映射的目标文件哈希仍有效；12份前向观察记录内容与原哈希一致。
- 原文件包QA记录门仍为PASS；更宽的行为记录门仍为UNVERIFIED，原因是缺完整v2.4模型运行回归基线。没有把旧未知项重新标为PASS。
- 新增12个隔离辅助工具检查，其中5项符合预期，7项不符合预期。数值只是本组反例结果，不是Skill总体成功率或统计缺陷率。
- 继续补测两项隔离发布附件场景：完整复制后回滚成功；复制中断后原文件备份有效，但配套回滚脚本无法启动恢复。只替换脚本测试路径，并在模拟目标注入一次Copy-Item错误，真实安装完全未动。
- 本次审核未重跑目标应用全部模式，也未新建真实生产成果；过去的CLI显式只读审计仅支持该单例和宿主范围。

真实命令、输入和输出见run_audit.py、audit-results.json及logs。probe中的target_app标签和证据文件是明确标注的模拟记录，只测试记录结构，不作为真实应用运行证据。

## 3. 需要修复的发现

### F-01 / P2：不合法的模式与强度组合可以跳过回归门

入口第30行要求恢复、迁移、部署、重构等使用FULL。gate只检查mode/profile各自属于枚举，没有验证组合；第176–177行仅凭profile=LIGHT就允许regression=N/A。

实测：mode=DEPLOY、profile=LIGHT、scope=DEPLOYMENT，填齐其他检查与有效证据文件哈希，把regression标N/A，gate返回PASS。MIGRATE/LIGHT/BEHAVIOR同样返回PASS。FULL UPDATE的相同N/A则正确BLOCKED，说明缺口确实由错误强度标签触发。

影响：用户或代理误填强度时，记录门会接受与Skill合同不一致的验收豁免。PASS仍只代表记录范围，不能独立证明发布资格；这一边界不能替代必要组合检查。

建议：建立模式/影响/强度的有效组合规则；regression豁免需有符合模式的适用性依据，不仅依据LIGHT字符串。以本次两个输入作为回归用例。证据：logs/deploy-light-skips-regression.json、logs/migrate-light-skips-regression.json；位置：scripts/seh_checks.py第147–149、175–179行。

### F-02 / P2：Markdown依赖识别会漏检和误报

第97行只用正则匹配内联链接，没有处理引用式链接，也没有排除代码围栏中的示例。

实测1：Skill要求读取`[required guide][guide]`，并定义`[guide]: missing.md`，目标缺失；inspect返回PASS且links为空。实测2：有效Skill只在明确标为示例的markdown代码围栏写`[example](missing.md)`，并不依赖该文件；inspect返回FAIL。普通内联缺失链接的对照检查则正确FAIL。

影响：既可能让必需流程缺失的Skill通过，也可能阻止没有依赖错误的Skill。引用式链接属于正常Markdown写法，不是复杂平台语法。

建议：正确区分正文依赖与代码示例，处理常见引用式链接；无法解析的必要依赖写UNVERIFIED，不能直接当作不存在。证据：logs/reference-style-missing.json、logs/literal-code-link.json；位置：scripts/seh_checks.py第93–108行。

### F-03 / P2：入口类型和版本检查存在漏检

实测1：实际存在但为空的VERSION文件，inspect返回PASS、version=""。第111行以`if version`作为检查条件，空字符串直接跳过校验；“没有可选文件”与“存在无效文件”应分开。

实测2：frontmatter为`description: []`时，inspect返回PASS；正式检查器拒绝并报告“Description must be a string, got list”。plain_fields把YAML源当文本字符串，未识别这是集合类型。检查器已声明不是通用YAML解析器，这个声明合理，但遇到不支持的输入应明确拒绝或标未验证，而非报告有效。

影响：未完成版本或宿主不能接受的入口可能获得结构PASS。本次真实SEH文件的版本和description正确，此发现不表示当前已安装源无效。

建议：文件存在时强制非空版本；对可支持标量输入明确检查，对集合/未知类型拒绝或交给正式验证器。证据：logs/empty-version.json、logs/sequence-description.json、logs/official-sequence-description.txt；位置：scripts/seh_checks.py第79–86、109–112行。

### F-04 / P3：schema_version的类型未校验

把schema_version=1改为JSON布尔值true，gate仍返回PASS，因为Python中True与1比较相等。此问题不直接改变当前有效记录的覆盖，但让错误记录协议类型被接受。

建议：明确要求整数1，并拒绝bool及其他类型；增加严格字段类型与错误记录测试。证据：logs/boolean-schema-version.json；位置：scripts/seh_checks.py第145行。

### F-05 / P2：发布附件在安装中断后缺少可直接使用的回滚记录

此发现针对delivery/seh-v3.0.0的sync_local.ps1和rollback_local.ps1，不属于已安装的14文件Skill包代码。

sync_local.ps1第31–41行先替换目标文件，第43行才写local-installation.json；rollback_local.ps1启动就读取该记录。若复制中途失败，备份存在，但记录还没有产生，配套回滚脚本无法读取Before/Installed清单。

隔离实测：在两个脚本副本中仅替换目标/项目路径，不指向真实安装。正常完整复制后，记录存在、原文件能恢复、本次新增VERSION移除，结果通过。另在SKILL.md替换成功后，对VERSION复制注入失败，确认旧备份哈希仍有效；local-installation.json不存在，回滚脚本报找不到记录，目标SKILL.md仍是新内容。故问题是自动恢复入口不完整，不是旧文件数据已经丢失；可以人工从备份恢复。

建议：修改任何目标前持久化恢复计划，逐文件记录写入状态；失败时用已持久化计划恢复或提供明确可执行的手动步骤。用本次完整/中断两个对照场景回归，保留后续改动保护。证据：probe_recovery.ps1、recovery-probe-results.json；位置：发布附件sync_local.ps1第31–43行和rollback_local.ps1第2行。

## 4. 不应误判为缺陷的限制

gate不能判断证据论证是否真实或充足，这一点入口与参考明确声明。给任意文件加target_app标签并不自动证明真的运行过应用，最终仍需核对内容和目标环境。不能把这种声明过的边界另写成已经发现的语义认证漏洞。

纯指令Skill无需自动状态引擎、注册表或固定24目录；v3.0.0已按任务适用，并准确说明可选集成。README/manifest保留unverified也符合当前全量目标验证不足的事实，不构成结构不完整。

现有12个前向请求是真实代理执行，有产物和保存成果检查，不只是标题匹配；但大多数围绕文本清理/计数，跨度覆盖模式、领域复杂度较窄。下一轮应优先选一个真实复杂Skill验证来源冲突、跨模块依赖及恢复，不能把12例算为所有生产环境均验证。

当前QA记录通过task_id与项目文件组织追踪，未在gate协议中强制绑定Skill ID/源版本/源哈希/目标环境；源变化后废弃旧PASS主要依赖调用者核对。这是可进一步改善的证据追踪设计，不是本次实测发现的“当前记录已过时”。

上一轮部署回滚附件只做过语法检查。此次补测确认正常隔离回滚可用，并发现F-05的中断恢复缺口；不能由成功路径推断所有恢复场景通过。该附件不在14文件运行包中，不混同为SEH指令本体缺陷。

## 5. 必要性与最终状态

对当前项目，SEH仍值得保留：已有多版本包、来源整合、平台迁移/安装和能力恢复，来源、CR、保真与证据分层能约束真实问题。与通用skill-creator相比，价值集中在长期治理、旧能力保持、版本协调和发布/恢复证据；简单创建修订使用LIGHT，避免每项工作都引入完整行政流程。没有对照数据，不能宣称遗漏率、返工或成本已下降。

task_result=COMPLETED；current_package_structure=PASS；source_install_integrity=PASS；representative_instruction_behavior=PASS（既有证据范围）；utility_boundary_qa=FAIL；辅助工具用于自动放行的相关阶段建议BLOCKED；full_production_qualification=UNVERIFIED。没有执行任何修复或发布，也没有修改原验收报告来掩盖本次发现。

下一步先做v3.0.1集中修复F-01至F-04，并同步修复发布附件F-05；重跑本组反例、现有28测试及两个隔离恢复场景，再补少量真实复杂Skill的行为/恢复用例。核心架构可继续使用；正式质量判定不能只依赖当前辅助工具PASS。完整平台验证和效果对照作为明确后续工作，不用继续增加泛化规则代替证据。
