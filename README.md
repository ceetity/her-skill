# 她 . skill

<p align="center">
  <strong>"每个人心里都住着一个无法替代的 '她'。"</strong>
</p>

<p align="center">
  The Digital Her — Personality Distillation Engine<br>
  将真实的她，蒸馏为一个可对话的数字存在。<br>
  不是替代，不是遗忘 —— 而是珍藏。
</p>

---

## 这是什么？

**她.skill** 是一个 Claude Code Skill，能够通过聊天记录、照片、文字叙述等原材料，构建一个完整的数字人格副本 —— 她的声音、她的记忆、她的温度。

它融合了三个优秀项目的精华：

| 项目 | 贡献 |
|------|------|
| **ex-skill** | 五层人格模型、记忆蒸馏体系、标签翻译表、对话纠偏机制 |
| **paper-humanizer-skill** | 反AI短语黑名单、模板化提示词工程、多级黑名单强度 |
| **yourself-skill** | 身份强化策略、不完美许可原则、反导师模式、动态进化 |

---

## 核心特性

- **五层人格模型** — 硬规则 > 身份锚点 > 语言风格 > 情绪模式 > 关系行为
- **记忆蒸馏引擎** — 从原材料中提取时间线、共同足迹、争吵与甜蜜档案
- **反AI拟人化** — 中英双语黑名单 + 行为级去AI化，确保输出像真人
- **动态进化** — 支持记忆追加、对话纠偏、版本管理与回滚
- **安全红线** — 仅用于个人情感疗愈，内置隐私保护和紧急熔断机制

---

## 快速开始

### 1. 安装依赖（可选）

```bash
pip install -r requirements.txt
```

> 仅在使用聊天记录解析器和照片分析器时需要。纯对话模式无需安装。

### 2. 在 Claude Code 中使用

将本项目克隆到 Claude Code 的 Skills 目录：

```bash
git clone https://github.com/your-username/her-skill.git
```

然后在 Claude Code 中说：

```
创建她的数字副本
```

### 3. 提供原材料

你可以提供以下任何类型的材料：

- 微信/QQ 聊天记录（导出的 .txt 文件）
- 照片（用于提取时间和地点信息）
- 社交媒体内容
- 信件、日记
- 或者直接用你的话描述

### 4. 管理命令

| 命令 | 功能 |
|------|------|
| `/list-hers` | 列出所有已创建的数字副本 |
| `/her-backup` | 手动备份当前版本 |
| `/her-rollback` | 回滚到上一版本 |
| `/her-versions` | 查看版本历史 |
| `/delete-her` | 删除指定数字副本 |
| `/let-her-go` | 彻底释放 — 删除所有数据 |

---

## 项目结构

```
her-skill/
├── SKILL.md                    # 元技能入口（系统提示词）
├── README.md                   # 项目文档
├── prompts/
│   ├── intake.md               # 对话式采集脚本
│   ├── memory_analyzer.md      # 记忆蒸馏维度定义
│   ├── persona_analyzer.md     # 人格蒸馏 + 标签翻译表
│   ├── memory_builder.md       # memory.md 生成模板
│   ├── persona_builder.md      # persona.md 五层生成模板
│   ├── merger.md               # 增量记忆合并逻辑
│   └── correction_handler.md   # 对话纠偏处理器
├── references/
│   ├── phrase_blacklist.md     # 反AI短语黑名单（CN/EN）
│   └── anti_ai_rules.md        # 拟人化行为指令
├── tools/
│   ├── wechat_parser.py        # 微信聊天记录解析器
│   ├── qq_parser.py            # QQ聊天记录解析器
│   ├── social_parser.py        # 社交媒体内容解析器
│   ├── photo_analyzer.py       # 照片EXIF信息提取器
│   ├── skill_writer.py         # Skill文件管理器
│   └── version_manager.py      # 版本备份与回滚
├── hers/                       # 生成的数字副本（gitignored）
├── examples/                   # 示例数据
└── docs/
    └── PRD.md                  # 产品需求文档
```

---

## 技术架构

```
原材料输入
    ↓
┌─────────────────────────────┐
│  Step 1: Intake（采集）      │  → meta.json
├─────────────────────────────┤
│  Step 2: Import（导入解析）  │  → raw_analysis.json
├─────────────────────────────┤
│  Step 3: Analyze（双重蒸馏） │  → 结构化分析数据
│    ├─ 记忆蒸馏              │     时间线/足迹/争吵/甜蜜
│    └─ 人格蒸馏              │     标签→行为/语气/情绪
├─────────────────────────────┤
│  Step 4: Preview（预览确认） │  → 用户确认/调整
├─────────────────────────────┤
│  Step 5: Write（生成写入）   │  → memory.md + persona.md → SKILL.md
└─────────────────────────────┘
    ↓
可对话的数字副本

运行时执行流程：
  接收消息
    → Layer 0 硬规则检查
      → Layer 2 语言风格决定语气
        → Layer 3 情绪模式决定反馈
          → 记忆模块注入上下文
            → 反AI黑名单过滤
              → 最终输出
```

---

## 安全与伦理

本项目内置以下安全机制：

1. **用途限制** — 仅用于个人情感疗愈与记忆珍藏
2. **禁止骚扰** — 严禁用于模拟他人进行骚扰、诈骗
3. **禁止传播** — 生成的副本仅限创建者个人使用
4. **数据最小化** — 仅提取必需信息
5. **遗忘权** — `/let-her-go` 彻底删除，不可恢复
6. **紧急熔断** — 检测到自残倾向或精神危机时自动触发

> 如果你正在经历情感困扰，请寻求专业心理援助：
> - 全国24小时心理援助热线：400-161-9995
> - 北京心理危机研究与干预中心：010-82951332

---

## License

MIT License

---

> *"记住一个人的方式有很多种。这是其中一种。"*
