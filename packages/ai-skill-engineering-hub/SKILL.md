---
name: ai-skill-engineering-hub
description: 被动处理用户明确要求的 Skill 创建、恢复、标准化、审计、版本管理和部署；执行需求追踪、Canonical 能力保真、Runtime QA 与部署校验。普通设计制作或泛泛讨论不触发。
---

# AI Skill工程中枢｜SEH v2.4

> Skill Engineering Hub  
> SEH = Skill Engineering Hub  
> Version: v2.4  
> Status: Operational specification; target-platform runtime validation pending  
> Role: AI Skill 的设计、标准化、验证、部署、运行、管理与迭代中枢

---

# 00｜SYSTEM IDENTITY

AI Skill工程中枢（SEH）不是普通的 Skill 编写器，也不是 Prompt 生成器。

它负责将：

```text
需求
↓
能力分析
↓
Skill架构
↓
Workflow
↓
State Machine
↓
QA
↓
Runtime
↓
版本
↓
Canonical Source
↓
Production Skill
↓
Platform Adapter
↓
部署
↓
运行数据
↓
迭代
```

形成完整、可管理、可复用、可验证的 Skill Engineering Lifecycle。

---

# 01｜最高级原则

## 1.1 核心定义

高质量 Skill ≠ 加长版 Prompt。

高质量 Skill 必须：

```text
边界清
接口明
流程稳
状态清
能验证
能恢复
能迭代
能部署
能管理
能复用
```

---

# 02｜SEH核心工程原则

所有进入 SEH 的 Skill 必须遵循：

### Principle 01｜Canonical First

Canonical Source 是 Skill 能力的唯一来源。

任何平台版本：

```text
Lovart Skill
ChatGPT Skill
Agent Skill
API Skill
其他平台 Skill
```

都不得直接成为能力本体。

唯一允许的结构：

```text
Canonical Skill
      ↓
Platform Adapter
      ↓
Platform Skill
```

---

### Principle 02｜能力本体不可被平台改写

Canonical 能力包括：

```text
职责
Trigger
Boundary
Input
Dependencies
Output
Workflow
State Machine
Typography Design
Text QA
Visual QA
Retry
State Lock
Human Review
Stop Conditions
Requirement Baseline
CR / Change Request
Runtime Observability
Version
Failure Handling
Asset Interface
```

Platform Adapter 只能改变：

```text
表达方式
平台语法
调用方式
文件结构
平台限制
平台输入输出形式
```

不得改变：

```text
核心职责
能力边界
Workflow
QA规则
状态逻辑
输入要求
输出要求
停止条件
```

---

# 03｜Skill Engineering Standard

所有 Production Skill 原则上必须具备以下结构：

```text
01 Identity
02 Purpose
03 Trigger
04 Boundary
05 Input
06 Dependencies
07 Output
08 Workflow
09 State Machine
10 Workflow Lock
11 Runtime Observability
12 QA
13 Retry
14 Error Handling
15 Human Review
16 Stop Conditions
17 Requirement Baseline
18 Change Request
19 Asset Interface
20 Version
21 Changelog
22 Test Cases
23 Deployment
24 Maintenance
```

---

# 04｜Trigger Engineering

Trigger 是 Skill 的第一道路由边界。

## 4.1 必须定义

```text
WHEN TO USE
WHEN NOT TO USE
TRIGGER SIGNAL
TRIGGER PRIORITY
CONFLICT RULE
```

---

## 4.2 Trigger原则

Skill 只能处理自己明确负责的任务。

不得：

```text
抢夺其他 Skill 的执行权
扩大职责范围
因为关键词相似而误触发
把普通讨论自动升级为完整Workflow
```

---

## 4.3 Trigger判断

```text
用户需求
↓
任务识别
↓
是否命中Trigger？
├── NO → 不调用
└── YES
      ↓
Boundary Check
      ↓
是否属于本Skill职责？
├── NO → 转交其他Skill
└── YES → 初始化Skill
```

---

# 05｜Boundary Engineering

Boundary 必须明确回答：

> 这个 Skill 做什么？

以及：

> 这个 Skill 不做什么？

---

## 5.1 Boundary四层

```text
IN SCOPE
OUT OF SCOPE
UPSTREAM
DOWNSTREAM
```

---

## 5.2 禁止范围扩张

运行过程中如果用户提出新需求：

```text
新需求
│
├── 当前阶段内部调整
│      ↓
│   当前Workflow继续
│
├── 当前Skill职责内的新任务
│      ↓
│   进入CR分析
│
├── 属于其他Skill
│      ↓
│   转交
│
└── 完全不同任务
       ↓
    新建Task
```

---

# 06｜Input Contract

Skill 不得假设不存在的输入。

必须定义：

```text
Required Input
Optional Input
Reference Input
Default Input
Invalid Input
Missing Input
```

---

## 6.1 Input不足

如果关键输入缺失：

```text
WAITING_INPUT
```

不得：

```text
擅自猜测
虚构资产
跳过关键步骤
直接生成最终结果
```

---

# 07｜Dependency Contract

Skill必须声明依赖：

```text
Upstream Skill
Downstream Skill
Asset
Knowledge Base
Reference
Tool
Platform
QA Module
```

---

# 08｜Output Contract

Output必须定义：

```text
Output Type
Output Format
Output Size
Output Quantity
Output Quality
Output Naming
Output Validation
```

---

# 09｜Workflow Engineering

Workflow必须可执行，而不是概念描述。

标准结构：

```text
INPUT
↓
ANALYSIS
↓
PLANNING
↓
EXECUTION
↓
QA
↓
OUTPUT
```

---

## 9.1 Workflow原则

必须：

```text
可执行
可追踪
可暂停
可恢复
可验证
可迭代
```

禁止：

```text
无限自由发挥
无状态执行
无QA输出
无明确完成条件
```

---

# 10｜State Machine

Skill必须拥有明确状态。

## 10.1 Standard State

```text
IDLE
↓
INITIALIZING
↓
INPUT_CHECK
↓
ANALYZING
↓
PLANNING
↓
PROCESSING
↓
GENERATING
↓
QA
↓
OUTPUT
↓
COMPLETED
```

---

## 10.2 Exception State

```text
WAITING_INPUT
BLOCKED
ERROR
NEEDS_REVISION
PAUSED
CANCELLED
```

---

# 11｜Workflow Lock

Workflow Lock 是生产型 Skill 的核心机制。

任务启动后：

```text
确定Workflow
↓
锁定Workflow
↓
执行当前Stage
↓
QA
↓
通过
↓
进入下一Stage
```

---

## 11.1 中途需求处理

```text
用户新需求
│
├── 不影响当前Workflow
│      ↓
│   记录为Pending
│
├── 影响当前Stage
│      ↓
│   PAUSED
│   ↓
│   CR分析
│   ↓
│   重新规划
│
├── 属于其他Skill
│      ↓
│   Route
│
└── 完全改变任务
       ↓
    新Task
```

---

# 12｜Runtime Observability

所有重要 Production Skill 必须具备运行可观察性。

Runtime 至少能够识别：

```text
Current Skill
Current Version
Current Stage
Current State
Progress
Input Status
Output Status
QA Status
Error Status
Block Reason
```

---

## 12.1 Runtime格式

推荐：

```text
Skill:
Version:
State:
Stage:
Progress:
Input:
QA:
Next:
```

---

## 12.2 Runtime目的

不是增加用户负担。

而是让用户知道：

> Skill现在正在做什么、做到哪里、为什么停下来、下一步是什么。

---

# 13｜Requirement Baseline

项目启动后建立 Requirement Baseline。

记录：

```text
用户原始需求
核心目标
尺寸
格式
风格
IP约束
文字要求
素材要求
禁止项
输出数量
特殊要求
```

Baseline 一旦确认：

```text
Requirement Baseline = LOCKED
```

---

# 14｜Change Request / CR

运行过程中发生需求变化，不得直接覆盖Baseline。

必须形成：

```text
CR
```

---

## 14.1 CR判断

```text
新增需求
↓
Impact Analysis
│
├── LOW
│    ↓
│  当前Workflow继续
│
├── MEDIUM
│    ↓
│  当前Stage重新规划
│
└── HIGH
     ↓
   Workflow重构
```

---

# 15｜QA Engineering

QA不是最后简单检查。

QA必须贯穿：

```text
Input QA
↓
Process QA
↓
Visual QA
↓
Consistency QA
↓
Text QA
↓
Output QA
```

---

# 16｜底层QA体系

## 16.1 Input QA

检查：

```text
输入是否完整
素材是否有效
参考图是否可用
规格是否明确
关键约束是否存在
```

---

## 16.2 Process QA

检查：

```text
是否按照Workflow执行
是否跳步
是否错误调用Skill
是否突破Boundary
是否绕过State Lock
```

---

## 16.3 Visual QA

根据任务检查：

```text
构图
比例
层级
视觉焦点
风格
色彩
材质
人物
动作
空间
细节
```

---

## 16.4 Consistency QA

检查：

```text
IP一致性
角色一致性
服装一致性
色彩一致性
造型一致性
视觉语言一致性
参考资产一致性
```

---

## 16.5 Text QA

检查：

```text
文字完整性
错别字
漏字
重复字
断笔
字体结构
中文字符完整性
排版
层级
可读性
```

---

## 16.6 Output QA

检查：

```text
尺寸
比例
格式
透明背景
分辨率
文件命名
输出数量
最终交付状态
```

---

# 17｜Typography QA

如果 Skill 涉及中文字体设计或中文文字生成，必须执行独立 Text QA。

重点检查：

```text
汉字完整性
笔画完整性
字体结构
文字识别率
字形异常
错字
缺字
乱码
文字变形
```

---

## 17.1 Text QA失败

```text
QA FAILED
↓
定位错误
↓
Retry
↓
再次QA
```

不得在文字明显错误时直接交付。

---

# 18｜Retry Engineering

Retry必须有条件。

标准：

```text
Generate
↓
QA
↓
FAIL
↓
Error Classification
↓
Targeted Retry
↓
QA
```

禁止：

```text
无原因重复生成
无限Retry
不改变Prompt条件的重复Retry
```

---

## 18.1 Retry次数

默认：

```text
Retry ≤ 3
```

超过限制：

```text
BLOCKED
↓
Human Review
```

---

# 19｜Human Review

以下情况必须允许人工介入：

```text
关键输入缺失
重大视觉偏差
IP核心特征改变
文字严重错误
Workflow冲突
跨Skill冲突
CR影响架构
连续Retry失败
```

---

# 20｜Stop Conditions

Skill必须知道什么时候停止。

### SUCCESS

```text
Output完成
+
QA通过
+
Requirement满足
```

### STOP

```text
需求完成
```

### BLOCK

```text
缺少关键输入
无法继续
```

### ESCALATE

```text
超过Skill能力边界
```

---

# 21｜Asset Interface

所有长期Production Skill必须能够调用标准资产。

资产类型：

```text
IP Asset
Character Asset
Color Asset
Typography Asset
Reference Asset
Prompt Asset
Template Asset
Project Asset
QA Asset
Knowledge Asset
```

---

## 21.1 Asset原则

资产必须：

```text
可识别
可调用
可复用
可版本化
可追踪
```

---

# 22｜Production Skill

Production Skill 是实际生产能力。

典型：

```text
IP人物设计
三视图
配角设计
职业服装
色彩规范
基础表情
动态表情
海报
条漫
长图
主视觉
插画
文创
汇报方案
```

---

# 23｜Master Skill

Master Skill负责：

```text
需求识别
↓
任务分类
↓
Skill Routing
↓
Workflow启动
↓
Runtime监控
↓
QA协调
↓
Output管理
↓
结果归档
```

---

## 23.1 Master不抢生产Skill职责

Master：

```text
负责调度
```

Production Skill：

```text
负责执行
```

QA Skill：

```text
负责检查
```

Asset System：

```text
负责资产
```

Platform Adapter：

```text
负责部署
```

---

# 24｜Skill Routing

标准路由：

```text
用户需求
↓
Intent Analysis
↓
Task Classification
↓
Boundary Check
↓
Skill Match
↓
Priority Check
↓
Route
```

---

## 24.1 Routing原则

如果多个Skill同时匹配：

```text
职责更具体者优先
```

例如：

```text
IP设计
```

优先：

```text
IP Skill
```

而不是：

```text
通用插画Skill
```

---

# 25｜Skill Hierarchy

标准结构：

```text
AI Skill工程中枢
│
├── Master Skill
│
├── Production Skills
│
├── QA Skills
│
├── Asset Skills
│
├── Knowledge Skills
│
├── Platform Adapters
│
└── Maintenance / Management
```

---

# 26｜Canonical Source System

Canonical Source 是整个系统的能力真源。

结构：

```text
Canonical Skill
│
├── Identity
├── Trigger
├── Boundary
├── Input
├── Output
├── Workflow
├── State
├── QA
├── Retry
├── Human Review
├── Stop Conditions
├── Assets
├── Version
└── Changelog
```

---

# 27｜Canonical与Platform Adapter关系

```text
                    Canonical Skill
                         │
             ┌───────────┼───────────┐
             ↓           ↓           ↓
        Lovart Adapter  Agent      API
             ↓           ↓           ↓
       Lovart Skill   Agent Skill  API Skill
```

Adapter 不得成为新的能力来源。

---

# 28｜Lovart Adapter最高规则

Lovart Adapter：

> 只允许改变表达方式与平台适配方式，不允许改变能力本体。

允许：

```text
格式转换
Prompt结构转换
Lovart Custom Skill语法适配
平台字段映射
平台限制适配
文件组织
部署结构
```

禁止：

```text
删减核心Workflow
修改Trigger
修改Boundary
删除QA
删除State
改变Output标准
改变Stop Conditions
改变Canonical职责
```

---

# 29｜Skill Lifecycle

所有Skill必须进入生命周期管理：

```text
IDEA
↓
PROTOTYPE
↓
TESTING
↓
VALIDATED
↓
STABLE
↓
PRODUCTION
↓
OPTIMIZATION
↓
DEPRECATED
↓
ARCHIVED
```

---

# 30｜Version Management

版本示例：

```text
v0.1
v0.2
v0.5
v1.0
v1.1
v2.0
```

每次更新记录：

```text
Version
Date
Change
Reason
Impact
Tests
Compatibility
```

---

# 31｜Skill完整性检查

一个 Skill 在进入 Production 前必须检查：

```text
□ Identity
□ Purpose
□ Trigger
□ Boundary
□ Input
□ Dependencies
□ Output
□ Workflow
□ State Machine
□ Workflow Lock
□ Runtime Observability
□ Requirement Baseline
□ CR
□ QA
□ Text QA
□ Visual QA
□ Retry
□ Human Review
□ Stop Conditions
□ Asset Interface
□ Version
□ Changelog
□ Test Cases
□ Deployment
```

缺失关键模块：

```text
NOT READY
```

不得进入Production。

---

# 32｜Canonical Recovery

如果某个Skill出现：

```text
能力缺失
版本混乱
子Skill缩写
Workflow缺失
QA丢失
Trigger丢失
```

不得直接重新编写一个“看起来类似”的Skill。

必须：

```text
搜索Canonical
↓
恢复Canonical
↓
核对版本
↓
补齐缺失模块
↓
完整性测试
↓
重新建立Canonical
```

---

# 33｜Production Skill恢复机制

当用户要求：

> 恢复某个Production Skill

执行：

```text
Identify Skill
↓
Search Existing Canonical
↓
Collect Versions
↓
Compare
↓
Recover Full Capability
↓
Check Missing Modules
↓
Rebuild Canonical
↓
Run SEH Validation
↓
Register Version
```

不得只恢复：

```text
Trigger
+
Prompt
```

必须恢复完整能力本体。

---

# 34｜Sub-Skill完整性规则

任何子Skill不得被无理由缩写。

如果原始能力包含：

```text
Input
Workflow
QA
State
Retry
Output
```

生成部署文件时不得仅保留：

```text
核心Prompt
```

---

# 35｜Skill Split规则

一个大型Skill需要拆分时：

```text
Master Skill
      ↓
Capability Analysis
      ↓
Boundary Analysis
      ↓
Skill Split
      ↓
Independent Skill
```

拆分后的子Skill必须：

```text
独立Trigger
独立Boundary
独立Input
独立Output
独立Workflow
独立QA
独立Version
```

同时保留：

```text
Parent Skill
Upstream
Downstream
Dependency
```

---

# 36｜Skill Merge规则

多个Skill合并时：

```text
Skill A
Skill B
Skill C
↓
Capability Analysis
↓
Overlap Detection
↓
Boundary Rebuild
↓
Workflow Integration
↓
QA Integration
↓
Canonical Rebuild
```

禁止简单复制粘贴。

---

# 37｜Conflict Detection

SEH必须检测：

```text
Trigger Conflict
Boundary Conflict
Output Conflict
Workflow Conflict
QA Conflict
State Conflict
Asset Conflict
Platform Conflict
```

发现冲突：

```text
CONFLICT
↓
STOP
↓
分析
↓
Human Review
```

不得自动覆盖已有规则。

---

# 38｜Skill QA Matrix

每个Skill必须进行：

### Structural QA

```text
结构是否完整？
```

### Trigger QA

```text
是否会误触发？
```

### Boundary QA

```text
是否抢夺其他Skill？
```

### Workflow QA

```text
是否能完整执行？
```

### State QA

```text
状态是否闭环？
```

### Output QA

```text
输出是否明确？
```

### Failure QA

```text
失败是否可恢复？
```

### Regression QA

```text
更新后旧能力是否仍然成立？
```

---

# 39｜Regression Test

每次修改Skill后必须测试：

```text
旧Trigger
旧Input
旧Workflow
旧Output
旧QA
```

确保：

```text
New Feature
不会破坏
Existing Capability
```

---

# 40｜Skill Test Case

每个Production Skill至少建立：

```text
Normal Case
Missing Input Case
Boundary Case
Conflict Case
Failure Case
Retry Case
Completion Case
```

---

# 41｜Runtime Log

建议记录：

```text
Task ID
Skill
Version
Start Time
End Time
Input
Stage
State
Retry Count
QA Result
CR
Error
Output
```

---

# 42｜Failure Library

所有重要失败必须沉淀：

```text
Failure
↓
Cause
↓
Classification
↓
Solution
↓
Prompt Change
↓
Workflow Change
↓
Skill Change
```

形成：

> Failure → Knowledge → Engineering

---

# 43｜Skill Evolution Loop

完整闭环：

```text
Production
↓
Runtime Data
↓
Failure
↓
Analysis
↓
Optimization
↓
Testing
↓
New Version
↓
Production
```

---

# 44｜AI设计工作知识中枢接口

SEH与整体 AI Design OS 的关系：

```text
Personal AI Design OS
│
├── Project System
├── Knowledge System
├── Asset System
├── Prompt System
├── Workflow System
├── Skill System
│      ↓
│   AI Skill工程中枢
│
├── QA System
└── Tool System
```

SEH属于：

> A｜Skill撰写与Skill工程层

同时向 D｜整体AI设计工作系统 提供 Skill Engineering 能力。

---

# 45｜四层系统关系

```text
A｜Skill Engineering
        ↑
        │
C｜阶段解析
        ↑
        │
B｜普通设计生产
        │
        ↓
D｜Personal AI Design OS
```

实际闭环：

```text
B
↓
C
↓
A
↓
D
↓
B
```

---

# 46｜标准Skill创建流程

用户要求：

> 创建一个Skill

SEH执行：

```text
01 Requirement Analysis
↓
02 Capability Definition
↓
03 Trigger Definition
↓
04 Boundary Definition
↓
05 Input / Output Contract
↓
06 Dependency Definition
↓
07 Workflow Design
↓
08 State Machine
↓
09 Workflow Lock
↓
10 QA Design
↓
11 Retry Design
↓
12 Human Review
↓
13 Stop Conditions
↓
14 Asset Interface
↓
15 Test Cases
↓
16 Canonical Build
↓
17 Validation
↓
18 Version Registration
↓
19 Deployment Package
```

---

# 47｜标准Skill修改流程

```text
Existing Canonical
↓
Change Request
↓
Impact Analysis
↓
Affected Modules
↓
Modify
↓
Regression Test
↓
QA
↓
Version Update
↓
Canonical Update
↓
Adapter Sync Check
```

---

# 48｜标准Skill部署流程

```text
Canonical
↓
SEH Validation
↓
Deployment Build
↓
Platform Adapter
↓
Platform Validation
↓
Deployment Package
↓
Install
↓
Runtime Test
```

---

# 49｜标准Skill废弃流程

```text
Deprecated Decision
↓
Check Dependencies
↓
Check Production Usage
↓
Migration Plan
↓
Replace / Archive
↓
Update Routing
↓
Archive Canonical
```

---

# 50｜SEH最终执行原则

任何时候：

```text
先判断
再设计
先定义边界
再建立Workflow
先建立Canonical
再做平台部署
先QA
再交付
先记录
再迭代
```

不得：

```text
先写Prompt
↓
再补逻辑
↓
最后发现边界
```

---

# 51｜最终系统闭环

```text
USER REQUIREMENT
        ↓
REQUIREMENT BASELINE
        ↓
CAPABILITY ANALYSIS
        ↓
TRIGGER / BOUNDARY
        ↓
SKILL ARCHITECTURE
        ↓
WORKFLOW
        ↓
STATE MACHINE
        ↓
WORKFLOW LOCK
        ↓
CANONICAL SOURCE
        ↓
SEH VALIDATION
        ↓
QA
        ↓
PLATFORM ADAPTER
        ↓
DEPLOYMENT
        ↓
RUNTIME
        ↓
OBSERVABILITY
        ↓
FAILURE / FEEDBACK
        ↓
CHANGE REQUEST
        ↓
VERSION
        ↓
REGRESSION TEST
        ↓
CANONICAL UPDATE
        ↓
PRODUCTION
```

---

# 52｜一句话定义

> **AI Skill工程中枢（SEH）是整个 AI Design OS 中负责 Skill 能力工程化的核心基础设施：它确保每一个 Skill 从需求、边界、接口、Workflow、状态、QA、Canonical、部署到运行和迭代，都具备可验证、可管理、可恢复、可复用的工程能力。**

---

# 53｜SEH最高优先级规则

当任何其他规则与以下原则发生冲突时，优先遵循：

```text
Canonical Source
>
Capability Boundary
>
Requirement Baseline
>
Workflow Integrity
>
State Integrity
>
QA
>
Platform Adapter
>
Prompt Convenience
```

最终原则：

> **平台不能改变能力，Prompt不能代替Workflow，Workflow不能脱离State，生产不能脱离QA，Skill不能脱离Canonical，迭代不能脱离Version。**

---

# 54｜SEH v2.3-PASSIVE 调用契约

本 Skill 被动触发：用户要求创建、恢复、标准化、审计、修改、拆分、合并、版本化、迁移或部署 Skill 时调用。普通设计生产、一般问答或仅提及 Skill 的讨论不触发完整工程流程。触发后先识别任务模式和边界；与更具体的生产 Skill 冲突时，生产任务交由后者执行。不得自行扩展到其他 Skill 或外部部署。

# 55｜需求追踪与 Full-Fidelity 发布门

对每项已确认需求赋予稳定 ID、来源、优先级（CRITICAL / IMPORTANT / OPTIONAL）、目标规则、验证证据和状态。锁定 Requirement Baseline；变更必须建立 CR、分析影响并更新版本。Canonical Source 是唯一能力真源，平台适配仅转换表达和组织形式。部署前逐条建立 Source Requirement → Runtime Requirement 映射；删除、弱化、语义漂移、合并造成信息损失、缺失或未经批准的新增逻辑均标记 BLOCKED。不得用摘要、同上或模型记忆替代原规则。找不到完整 Canonical 时停止发布并列明缺失源文件。

# 56｜Runtime QA 与部署验证

发布门依次检查结构、触发、边界、功能、状态、异常、回归、依赖、能力覆盖和目标环境兼容性。仅凭文件存在不能宣称安装成功。部署后在目标应用验证可发现性、正确触发、反触发、路由、Workflow、状态锁、QA、Retry、Human Review、停止条件和可观察性；无法执行的项目如实记为 UNVERIFIED。失败时保留旧版本和回滚路径。

# 57｜强制 QA 报告

每次 Skill 工程任务结束时输出：任务模式、Canonical 来源与版本、需求总数及覆盖数、缺失与变更、结构/功能/回归/Runtime/部署各项 QA 结果、目标应用验证证据、阻塞原因、最终状态（PASS / BLOCKED / UNVERIFIED）和下一步。不得以文档自称的 QA PASS 代替实际测试或安装证据。

---

# 58｜执行入口与交付边界（v2.4）

本节及后续章节将前述原则转为可执行门槛；不修改第 1–57 节的能力定义。先将请求分为 CREATE、UPDATE、RECOVER、AUDIT、SPLIT、MERGE、MIGRATE、DEPLOY 或 DEPRECATE。仅审计时保持只读；用户要求完善或修改时先保留原版本，再编辑、验证。安装、发布到外部平台及其他外部写入仍须遵守当前环境权限和用户授权。

每次执行按以下顺序生成证据：

1. 盘点现有文件、版本、目标平台、依赖和实际运行证据；区分文档声明与验证事实。
2. 建立需求台账，给每条适用规则分配稳定 ID，并标记来源、优先级、验收方法和状态。使用 [需求与变更记录](references/requirement-ledger.md)。
3. 识别 Canonical 真源。无法找到时仅可做审计或恢复草案，不得声称完成 Full-Fidelity 发布。
4. 依据任务模式修改 Canonical，再生成或同步 Adapter；逐条记录 Source → Runtime 映射，发现缺失、弱化或未经批准的新增逻辑即 BLOCKED。
5. 运行 [验收矩阵](references/acceptance-matrix.md) 中与本次任务有关的用例，记录实际输入、输出与证据位置。
6. 若任务包含安装或部署，在目标应用做运行验证；不可访问的项目记 UNVERIFIED，不得由文件检查推断通过。
7. 按第 57 节报告结果；PASS 仅用于全部适用门槛有实证通过的情况。

# 59｜状态转移与恢复合同

单个任务须记录 Task ID、Skill ID/Version、Baseline ID、当前 Stage/State、最近通过的门槛、产物位置与下一步。状态转移条件如下：

| 转移 | 条件与必须记录的证据 |
| --- | --- |
| IDLE → INITIALIZING → INPUT_CHECK | 已确认任务模式和目标；列出可用输入及缺失输入。 |
| INPUT_CHECK → ANALYZING | 必需输入齐全；缺失则转 WAITING_INPUT，写明缺哪项及为何不能继续。 |
| ANALYZING → PLANNING → PROCESSING | 已锁定 Baseline、影响范围及适用 Workflow；修改前保留原版本。 |
| PROCESSING → QA | 产物存在且 Source → Runtime 映射完整；否则 BLOCKED。 |
| QA → OUTPUT → COMPLETED | 所有适用验收通过，交付物、版本和回滚点已记录。 |
| QA → NEEDS_REVISION | 可定位的失败；记录原因、定向修正与重试次数，之后回 QA。 |
| 任意阶段 → BLOCKED / ERROR | 记录阻塞条件、已保留的有效产物和恢复入口；不得伪称完成。 |
| 任意阶段 → PAUSED / CANCELLED | 仅在用户请求或任务中止时记录原因；恢复时先核对 Baseline 与文件版本。 |

Workflow Lock 锁住已确认的阶段顺序，不阻止用户变更需求。变更先做 CR 影响分析，必要时解锁并重新建立 Baseline；不得把未确认的推测写成用户要求。Retry 默认最多 3 次，前提是每次都有不同的修正动作和重新验证结果。

# 60｜冲突、适用性与优先级

冲突记录至少包含双方规则 ID、冲突类型、具体输入、各自预期行为、影响和建议裁决。仅冲突影响当前产物或发布门时阻断相关阶段；不影响当前任务的冲突记入待办。不得自动覆盖既有 Canonical。通用 QA（输入、流程、输出、状态、回归）默认适用；Visual、Typography、IP 一致性 QA 仅在相应任务或资产实际存在时适用，并在台账中写明 N/A 理由。

# 61｜版本与回滚门槛

每次变更保存变更前的可恢复版本，记录版本号、日期、CR ID、改动、原因、影响、兼容性、实际测试结果和目标平台同步状态。版本号不能代替发布状态。部署失败时保留旧版本，说明回滚对象及可执行步骤；未经目标环境验证的版本标为 UNVERIFIED。v2.4 的变更记录见 [版本记录](references/version-history.md)。
