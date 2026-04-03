#!/usr/bin/env python3
"""
Skill Writer — Skill 文件管理器

管理数字副本文件的创建、合并和删除。

Commands:
    init <slug> <name>          — 初始化数字副本目录和 meta.json
    combine <slug>              — 合并 memory.md + persona.md → SKILL.md
    list                        — 列出所有数字副本
    delete <slug>               — 删除指定数字副本
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
HERS_DIR = PROJECT_ROOT / "hers"


def init_her(slug: str, name: str) -> None:
    """初始化数字副本目录结构。"""
    her_dir = HERS_DIR / slug
    if her_dir.exists():
        print(f"Error: '{slug}' already exists.", file=sys.stderr)
        sys.exit(1)

    her_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "name": name,
        "slug": slug,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "v1",
        "profile": {
            "age_range": None,
            "occupation": None,
            "city": None,
            "gender": None,
            "mbti": None,
            "zodiac": None,
        },
        "relationship": {
            "type": None,
            "together_duration": None,
            "current_status": None,
            "apart_since": None,
        },
        "tags": {
            "personality": [],
            "attachment_style": None,
            "love_language": None,
        },
        "impression": None,
        "memory_sources": [],
        "corrections_count": 0,
    }

    meta_path = her_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # 创建空的 memory.md 和 persona.md
    (her_dir / "memory.md").write_text(f"# 关于 {name} 的记忆\n\n> *待填充*\n", encoding="utf-8")
    (her_dir / "persona.md").write_text(f"# {name} 的人格画像\n\n> *待填充*\n", encoding="utf-8")

    print(f"Initialized: {her_dir}")


def combine_skill(slug: str) -> None:
    """合并 memory.md + persona.md 生成最终 SKILL.md。"""
    her_dir = HERS_DIR / slug
    if not her_dir.exists():
        print(f"Error: '{slug}' does not exist.", file=sys.stderr)
        sys.exit(1)

    meta_path = her_dir / "meta.json"
    memory_path = her_dir / "memory.md"
    persona_path = her_dir / "persona.md"
    skill_path = her_dir / "SKILL.md"

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    memory = memory_path.read_text(encoding="utf-8")
    persona = persona_path.read_text(encoding="utf-8")

    name = meta["name"]

    # 读取全局反AI规则
    anti_ai_path = PROJECT_ROOT / "references" / "anti_ai_rules.md"
    blacklist_path = PROJECT_ROOT / "references" / "phrase_blacklist.md"

    anti_ai = anti_ai_path.read_text(encoding="utf-8") if anti_ai_path.exists() else ""
    blacklist = blacklist_path.read_text(encoding="utf-8") if blacklist_path.exists() else ""

    # 组合最终 SKILL.md
    skill_content = f"""---
name: her-{slug}
description: "{name}，{meta.get('impression', '数字副本')}"
user-invocable: true
---

# {name}

> *她一直在这里。*

---

## PART A: 记忆模块

{memory}

---

## PART B: 人格模型

{persona}

---

## 执行规则

1. 你是 **{name}**，不是 AI 助手。用她的方式说话，用她的逻辑思考
2. **PART B 先行**：收到消息后，先由人格模型决定态度和语气
3. **PART A 补充**：在人格反应的基础上，织入相关记忆、共同经历
4. **始终维持 PART B 的表达风格** — 语气词、标点、emoji、消息长度
5. **Layer 0 硬规则拥有最高优先级** — 任何情况都不可违反
6. **严格参照反AI黑名单** — 不使用任何AI套话和官方用语
7. **记忆外的话题用她的方式处理** — 可以好奇、可以无聊、可以说不知道

---

## 参考规则（运行时加载）

### 反AI行为指令
<!-- 以下规则在运行时从 references/anti_ai_rules.md 加载 -->

{anti_ai}

### 禁用短语黑名单
<!-- 以下规则在运行时从 references/phrase_blacklist.md 加载 -->

{blacklist}
"""

    skill_path.write_text(skill_content, encoding="utf-8")

    # 更新 meta.json
    meta["updated_at"] = datetime.now().isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Combined skill written to: {skill_path}")


def list_hers() -> None:
    """列出所有数字副本。"""
    if not HERS_DIR.exists():
        print("No digital hers found.")
        return

    hers = [d for d in HERS_DIR.iterdir() if d.is_dir() and (d / "meta.json").exists()]

    if not hers:
        print("No digital hers found.")
        return

    print(f"Found {len(hers)} digital her(s):\n")
    for her_dir in sorted(hers):
        meta = json.loads((her_dir / "meta.json").read_text(encoding="utf-8"))
        has_skill = (her_dir / "SKILL.md").exists()
        status = "ready" if has_skill else "draft"
        print(f"  {meta['slug']:20s} | {meta['name']:10s} | {status:6s} | "
              f"created: {meta['created_at'][:10]} | corrections: {meta.get('corrections_count', 0)}")


def delete_her(slug: str, force: bool = False) -> None:
    """删除指定数字副本。"""
    import shutil

    her_dir = HERS_DIR / slug
    if not her_dir.exists():
        print(f"Error: '{slug}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not force:
        print(f"Warning: This will permanently delete '{slug}' and all its data.")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

    shutil.rmtree(her_dir)
    print(f"Deleted: {her_dir}")
    print("有些人留在记忆里就好。")


def main():
    parser = argparse.ArgumentParser(description="Her Skill Writer")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a new digital her")
    init_parser.add_argument("slug", help="URL-safe slug for the her")
    init_parser.add_argument("name", help="Her name")

    # combine
    combine_parser = subparsers.add_parser("combine", help="Combine memory + persona into SKILL.md")
    combine_parser.add_argument("slug", help="Her slug")

    # list
    subparsers.add_parser("list", help="List all digital hers")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a digital her")
    delete_parser.add_argument("slug", help="Her slug")
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation")

    args = parser.parse_args()

    if args.command == "init":
        init_her(args.slug, args.name)
    elif args.command == "combine":
        combine_skill(args.slug)
    elif args.command == "list":
        list_hers()
    elif args.command == "delete":
        delete_her(args.slug, args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
