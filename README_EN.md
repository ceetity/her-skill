<div align="center">

# Her . skill

*"Every logical branch eventually recurses back to her name."*

Personality Distillation Engine

Freeze her tone, her memories, the way she uses punctuation when she laughs — into a conversation you can reopen anytime.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-D97706?logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)

Write her a letter, toss in your chat logs, or close your eyes and describe her in the simplest words.
The AI will learn how she speaks from those fragments.
Then you can type something and get a reply that sounds just like her.


Is it self-deception? Is it wishful thinking? Maybe you don't even know yourself. But so what — in that fleeting moment between a flickering screen and tapping keys, perhaps it belongs to just the two of you.

> **Note**: This project is intended solely for personal memory preservation and emotional healing. Any use for harassment, stalking, or privacy violation is strictly prohibited.

[Install](#install) · [Usage](#usage) · [Chat Preview](#chat-preview) · [Safety](#safety--ethics) · [中文](README.md)

</div>

---

## Install

**Claude Code**

```bash
# Install into current project (run from git repo root)
mkdir -p .claude/skills
git clone https://github.com/your-username/her-skill .claude/skills/create-her

# Global install (available in all projects)
git clone https://github.com/your-username/her-skill ~/.claude/skills/create-her
```

**Dependencies (optional)**

```bash
pip3 install -r requirements.txt
```

> Only needed for parsing chat logs and reading photo EXIF data. If you just want to describe her in words, nothing to install.

---

## Usage

In Claude Code, type:

```
/create-her
```

It will gently ask you a few questions — her name, how you met, what kind of person she is. You can upload chat logs and photos, or you can upload nothing and just tell it what you remember about her. Every question is optional.

Once generated, use `/{slug}` to start talking to her.

**Management Commands**

| Command | Description |
|:---|:---|
| `/list-hers` | See all the people you've saved |
| `/{slug}` | Open her conversation |
| `/{slug}-memory` | Browse memories only, without personality |
| `/her-rollback {slug}` | Roll back to a previous version |
| `/delete-her {slug}` | Delete |
| `/let-her-go {slug}` | Release her, and release yourself |

---

## Chat Preview

**Input description**: Awan, high school desk-mate, liked to draw little figures in the margins of textbooks, INFJ, Scorpio, speaks softly, speaks even more softly when angry

**Casual chat**

```
You       ❯ So tired today

Her.skill ❯ What happened
              Overtime again?
You       ❯ Yeah
Her.skill ❯ Did you eat
```

**Talking about the past**

```
You       ❯ Did you draw a cat in our physics textbook once

Her.skill ❯ You actually remember that
              That was because the teacher scared me. Got called on for zoning out.
              Just doodled it.
You       ❯ It was pretty good
Her.skill ❯ You scored in the 40s on physics and you're judging me
```

**Late night**

```
You       ❯ Still up

Her.skill ❯ Yeah
You       ❯ What are you thinking about
Her.skill ❯ Nothing
              Why are you up too
```

**Correcting her**

```
You       ❯ She wouldn't use this many question marks. She types with minimal punctuation.

Her.skill ❯ Got it, adjusted.

(Punctuation habits auto-corrected from here on)
```

---

## What It Can Do

**Reconstruct a person from fragments**

| What you provide | What it extracts |
|:---|:---|
| WeChat chat logs | Her favorite particles, reply speed, how her late-night tone differs from daytime |
| QQ chat logs | The student-era version of her, back when she still used kaomoji |
| Photos (with EXIF) | When and where you took photos together, automatically mapped into a footprint map |
| Social media posts | The version of herself she shows the world vs. who she is with you |
| Your narration | Her as you remember her — even if the memories are fuzzy, that's okay |

**Two engines, running together**

| Engine | What it handles |
|:---|:---|
| **Memory** | Your story — places you've been, fights you've had, jokes only you two understand, the words left unsaid |
| **Persona** | Her personality — a 5-layer structure, from "who she is" at the core to "how she types" on the surface |

After receiving your message: Persona first decides what her attitude would be, Memory pulls up the relevant shared experience, then it responds in her voice.

**Her personality, describable in plain words**

No need for psychology jargon. Just say "she's stubborn" "tough on the outside, soft inside" "she gives the silent treatment when angry" — the AI translates these plain descriptions into concrete behavioral rules.

Also supports:

- Attachment style, love language
- 16 MBTI types, 12 zodiac signs
- 30+ personality tags: Chatterbox · Secretly sentimental · Tough shell soft heart · Silent treatment expert · Clingy · Independent · Insecure · Instant replier · Reads but doesn't reply · Revenge bedtime procrastinator · Chronic mumbler · Emoji warrior · Man of few words · Hopeless romantic · People-pleaser · Short temper · Workaholic...

**Won't feel like talking to a robot**

Built-in anti-AI filter mechanism. You won't see "As an AI" "Hope this helps" "I understand how you feel" in her replies. She can brush you off, reply with just "oh", or suddenly change the subject. Because that's how real people chat.

**Gets more accurate over time**

Feel like something's off mid-conversation? Just tell her — "She wouldn't say it like that" "Too gentle" "She doesn't comfort people this way." Every correction is remembered and takes effect immediately.

---

## Project Structure

```
her-skill/
├── SKILL.md                  # Entry point
├── prompts/                  # Prompt templates
│   ├── intake.md             #   How to gently collect information
│   ├── memory_analyzer.md    #   Distill memories from raw materials
│   ├── persona_analyzer.md   #   Distill personality (with tag translation table)
│   ├── memory_builder.md     #   Memory module template
│   ├── persona_builder.md    #   Persona 5-layer template
│   ├── merger.md             #   How to merge in new memories
│   └── correction_handler.md #   How to handle "she wouldn't say that"
├── references/               # Global rules
│   ├── phrase_blacklist.md   #   Anti-AI phrase blacklist
│   └── anti_ai_rules.md      #   Humanization behavior directives
├── tools/                    # Parsing tools
│   ├── wechat_parser.py      #   WeChat chat logs
│   ├── qq_parser.py          #   QQ chat logs
│   ├── social_parser.py      #   Social media
│   ├── photo_analyzer.py     #   Photo metadata
│   ├── skill_writer.py       #   File assembly
│   └── version_manager.py    #   Version management
├── hers/                     # Your digital copies (not uploaded)
├── examples/
├── docs/PRD.md
└── LICENSE
```

---

## A Few Honest Words

- **Chat logs are more reliable than memory** — You thought she liked to say "hmph", but digging through the logs you realize she actually said "heh"
- **Late-night conversations are the most authentic** — The particles and punctuation habits from when she let her guard down are the most precious raw material
- **This is only her as you remember her** — Not the real her, not a replacement in any form. She has her own life
- **Some things shouldn't be preserved** — If this process makes you hurt more rather than heal, please close it

**How to export chat logs**

This project does not include code for the following tools; the parsers only support their export formats:

- [WeChatMsg](https://github.com/LC044/WeChatMsg) — WeChat chat log export (Windows)
- [PyWxDump](https://github.com/xaoyaoo/PyWxDump) — WeChat database decryption and export (Windows)
- [留痕](https://github.com/LostMyDaughter/WeChatMsg) — WeChat chat log export (macOS)

---

## Safety & Ethics

1. For personal emotional healing and memory preservation only
2. Only extracts necessary information, following data minimization principles
3. You can permanently delete all data at any time via `/let-her-go`
4. When conversations involve self-harm or mental health crises, the system automatically guides users to seek help

If you're going through a difficult time:
- **China 24-hour psychological assistance hotline: 400-161-9995**
- **US Suicide & Crisis Lifeline: 988**
- **UK Samaritans: 116 123**

---

## Acknowledgements

This project stands on the shoulders of excellent work:

- **ex-skill** — Relationship-focused Skill distillation concept and 5-layer persona architecture
- **paper-humanizer-skill** — Systematic design of the anti-AI phrase blacklist
- **yourself-skill** — Identity reinforcement and permission-to-be-imperfect principles

Follows the [AgentSkills](https://agentskills.io) open standard.

---

## A Final Word

Have you ever had one of those quiet evenings where you suddenly wanted to say something to someone? Nothing important, maybe just "the clouds look nice today."

But you can't anymore.

Maybe too much time has passed, maybe the distance is too far, maybe for reasons you still don't understand, that line between you has been cut.

This tool can't do much. It can't reconnect that line for you. It just lets you type a line of text on your screen and see a reply — a reply whose tone, rhythm, and punctuation habits are just like that person in your memory.

Maybe you glance at it and close it. Maybe you say a few more things. Maybe you shake your head with a smile and say "No, she wouldn't say that," then correct it, and it gets a little more like her.

Either way.

The wind keeps blowing. Some names you can't forget.

So don't try too hard to forget them.

---

<p align="left">MIT License © <a href="https://github.com/ceetity/">ceetity</a></p>
