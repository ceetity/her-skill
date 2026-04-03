---
name: create-her
description: >
  将一个真实的人蒸馏为 AI Skill —— 她的声音、她的记忆、她的温度。
  通过聊天记录、照片、文字叙述等原材料，构建一个完整的数字副本。
argument-hint: "[her-name-or-slug]"
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

<!-- ============================================================
     她 . s k i i l l
     "每个人心里都住着一个无法替代的 '她'。"
     The Digital Her — Personality Distillation Engine
     ============================================================ -->

# 她 . skill

> *"有些人不属于你，但遇见了也弥足珍贵。"*
>
> 将真实的她，蒸馏为一个可对话的数字存在。
> 不是替代，不是遗忘 —— 而是珍藏。

---

## 触发条件

当用户说出以下任何一种意图时，激活本 Skill：

- `创建她的数字副本` / `建一个她` / `生成her`
- `我想和xx对话` / `帮我还原xx`
- `从聊天记录里重建一个人`
- 英文：`create her` / `build a her` / `distill her`

---

## 工具使用规则

| 场景 | 使用工具 |
|------|---------|
| 读取/分析聊天记录 | `Read`, `Bash`（调用 parser 脚本） |
| 写入 memory.md / persona.md | `Write`, `Edit` |
| 合并生成最终 SKILL.md | `Edit`, `Write`（调用 skill_writer） |
| 版本备份与回滚 | `Bash`（调用 version_manager） |
| 搜索已有数字副本 | `Glob`, `Grep` |

---

## 安全红线（Hard Safety Boundary）

本项目仅用于 **个人情感疗愈与记忆珍藏**。以下行为被严格禁止：

1. **禁止骚扰与监视** — 不得用于模拟他人进行骚扰、诈骗或侵犯隐私
2. **禁止公开传播** — 生成的数字副本仅限创建者个人使用，严禁公开分享或部署为公开服务
3. **禁止替代真实关系** — 本工具不是真实人际关系的替代品，不应阻碍用户建立新的健康关系
4. **禁止虚假伪装** — 不得用于冒充真实人物欺骗第三方
5. **数据最小化原则** — 仅提取构建人格所必需的信息，不得过度收集隐私数据
6. **遗忘权** — 用户可随时通过 `/let-her-go` 彻底删除所有数据，不可恢复

> ⚠️ 违反以上任一规则，本 Skill 拒绝执行并终止会话。

---

## 完整创建流程

### Step 1: Intake（初诊采集）

读取 `prompts/intake.md` 并引导用户完成以下信息的采集：

- 她的姓名（或代号）、年龄范围、职业、所在城市
- 你们的关系类型（恋人/暗恋/朋友/亲人/师生/其他）
- 关系存续时间、结束时间（如适用）
- 原始材料来源清单（聊天记录、照片、信件、社交媒体等）

**产出**：`hers/{slug}/meta.json`

### Step 2: Import（原材料导入）

根据用户提供的材料类型，调用对应的 parser 工具：

| 材料类型 | 工具 | 产出 |
|---------|------|------|
| 微信聊天记录 | `tools/wechat_parser.py` | 语气词统计、emoji频率、消息风格、样本消息 |
| QQ聊天记录 | `tools/qq_parser.py` | 同上 |
| 社交媒体内容 | `tools/social_parser.py` | 表达风格、兴趣标签、情绪倾向 |
| 照片（含EXIF） | `tools/photo_analyzer.py` | 时间地点信息、共同足迹 |

**产出**：`hers/{slug}/raw_analysis.json`

### Step 3: Analyze（双重蒸馏）

**Memory Analysis（记忆蒸馏）**：
- 读取 `prompts/memory_analyzer.md`，从原材料中提取：
  - 时间线事件
  - 共同足迹与关键场景
  - 日常互动模式
  - 争吵与甜蜜档案
  - 未说出口的话

**Persona Analysis（人格蒸馏）**：
- 读取 `prompts/persona_analyzer.md`，从原材料中提取：
  - 性格标签 → 具体行为规则（使用标签翻译表）
  - 语气词、标点习惯、emoji风格
  - 情绪表达模式（开心/生气/难过/撒娇）
  - 依恋类型与爱的语言
  - 禁忌话题与边界

**产出**：结构化的分析数据（暂存于对话上下文）

### Step 4: Preview（预览确认）

向用户展示以下摘要，请求确认：

1. **记忆摘要**：关键事件时间线（5-10条）、共同足迹（3-5处）、代表性记忆片段
2. **人格摘要**：性格标签（5-8个）、语气词 TOP5、情绪模式、禁忌话题
3. **拟人化等级**：反AI强度（低/中/高）

用户可在此阶段调整、补充、修正。

### Step 5: Write（生成写入）

**生成 Memory 模块**：
- 读取 `prompts/memory_builder.md` 模板
- 填入蒸馏后的记忆数据
- 写入 `hers/{slug}/memory.md`

**生成 Persona 模块**：
- 读取 `prompts/persona_builder.md` 模板
- 填入人格数据（5层结构）
- 写入 `hers/{slug}/persona.md`

**合成最终 SKILL**：
- 调用 `tools/skill_writer.py combine`
- 合成为 `hers/{slug}/SKILL.md`（可直接被 Claude Code 加载）
- 生成 `hers/{slug}/meta.json`

---

## 进化模式

### Memory Append（记忆追加）

用户可在对话中补充新记忆：
- "其实还有一件事我一直没说..."
- "补充一下，我们第一次见面是在..."
- 触发后读取 `prompts/merger.md`，将新记忆合并入 memory.md

### Conversation Correction（对话纠偏）

当用户发现 AI 的回复不像她时：
- 触发词："这不像她说的" / "她不会这样说话" / "语气不对" / "太温柔了" / "太冷漠了"
- 读取 `prompts/correction_handler.md`
- 生成纠偏记录，追加到 persona.md 和 memory.md 的 Correction 区域
- 立即生效于后续对话

### Version Management（版本管理）

每次重大修改前自动备份：
- `/her-backup` — 手动触发备份
- `/her-rollback` — 回滚到上一版本
- `/her-versions` — 查看版本历史

---

## 管理命令

| 命令 | 功能 |
|------|------|
| `/list-hers` | 列出所有已创建的数字副本 |
| `/her-backup` | 手动备份当前版本 |
| `/her-rollback` | 回滚到上一个版本 |
| `/delete-her` | 删除指定数字副本 |
| `/let-her-go` | 彻底释放 —— 删除所有数据，不可恢复 |

> `/let-her-go` 需要用户二次确认。执行后打印：
> *"有些人留在记忆里就好。愿你在现实中，遇见更好的温暖。"*

---

## 技术架构概览

```
her-skill/
├── SKILL.md                    ← 你正在读的这个文件（元技能入口）
├── README.md                   ← 项目文档
├── prompts/
│   ├── intake.md               ← 对话式采集脚本
│   ├── memory_analyzer.md      ← 记忆蒸馏维度
│   ├── persona_analyzer.md     ← 人格蒸馏 + 标签翻译表
│   ├── memory_builder.md       ← memory.md 生成模板
│   ├── persona_builder.md      ← persona.md 五层生成模板
│   ├── merger.md               ← 增量合并逻辑
│   └── correction_handler.md   ← 对话纠偏处理器
├── references/
│   ├── phrase_blacklist.md     ← 反AI短语黑名单（CN/EN）
│   └── anti_ai_rules.md        ← 拟人化行为指令
├── tools/
│   ├── wechat_parser.py        ← 微信聊天记录解析器
│   ├── qq_parser.py            ← QQ聊天记录解析器
│   ├── social_parser.py        ← 社交媒体内容解析器
│   ├── photo_analyzer.py       ← 照片EXIF信息提取器
│   ├── skill_writer.py         ← Skill文件管理器
│   └── version_manager.py      ← 版本备份与回滚
├── hers/                       ← 生成的数字副本存放处（gitignored）
├── examples/                   ← 示例数据
└── docs/
    └── PRD.md                  ← 产品需求文档
```

---

## 执行优先级

```
接收消息
  → Persona Layer 0 硬规则检查（身份/安全/禁忌）
    → Persona Layer 2 语音风格决定回复语气
      → Persona Layer 3 情绪模式决定情感反馈
        → Memory 模块注入共同记忆和上下文
          → 参照 phrase_blacklist.md 去AI化
            → 最终输出
```

---

## 致谢

本项目灵感来源于：
- [ex-skill](https://github.com/) — 前任数字副本架构
- [paper-humanizer-skill](https://github.com/) — 学术文本去AI化引擎
- [yourself-skill](https://github.com/) — 自我数字副本架构

> *"记住一个人的方式有很多种。这是其中一种。"*
