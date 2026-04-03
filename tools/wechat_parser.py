#!/usr/bin/env python3
"""
WeChat Chat Log Parser — 微信聊天记录解析器

从导出的微信聊天记录中提取：
- 语气词频率统计
- Emoji 使用频率
- 标点习惯分析
- 消息长度分布
- 样本消息提取

Usage:
    python wechat_parser.py <input_file> --target <target_name> [--output <output_file>]
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


# 语气词模式
PARTICLE_PATTERNS = [
    r"嗯+", r"哦+", r"噢+", r"哈哈+", r"hh+",
    r"嘿嘿", r"嘿", r"唉+", r"呜呜+", r"嘤嘤+",
    r"哇+", r"哎+", r"呀+", r"吧", r"呢",
    r"嘛", r"咯", r"呐", r"啦", r"滴",
    r"鸭", r"惹", r"惹", r"惹", r"呗",
]

# Emoji 正则（简化版，匹配常见 emoji）
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"
    "\u3030"
    "]+",
    flags=re.UNICODE,
)

# 标点分类
PUNCT_MAP = {
    "period": r"[。]",
    "exclamation": r"[！!]",
    "question": r"[？?]",
    "ellipsis": r"[…]{2,}|[。]{2,}|\.+",
    "tilde": r"[~～]+",
    "comma": r"[，,]",
}


def parse_messages(text: str, target: str) -> list[dict]:
    """
    解析微信导出的聊天记录。
    支持多种常见导出格式。

    每条消息解析为:
    {
        "time": "datetime string or None",
        "sender": "sender name",
        "content": "message content",
        "is_target": True/False
    }
    """
    messages = []
    lines = text.strip().split("\n")

    # 常见格式 1: "2024-01-01 12:00:00 Name\n content"
    # 常见格式 2: "Name 12:00\n content"
    # 常见格式 3: "[12:00] Name: content"

    current_msg = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 尝试匹配带头部信息的行
        # 格式: 日期 时间 发送者
        header_match = re.match(
            r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)",
            line,
        )
        if header_match:
            if current_msg:
                messages.append(current_msg)
            time_str = header_match.group(1)
            sender = header_match.group(2).strip()
            current_msg = {
                "time": time_str,
                "sender": sender,
                "content": "",
                "is_target": sender == target,
            }
            continue

        # 格式: [时间] 发送者: 内容
        bracket_match = re.match(r"\[([^\]]+)\]\s*([^:：]+)[：:]\s*(.+)", line)
        if bracket_match:
            if current_msg:
                messages.append(current_msg)
            current_msg = {
                "time": bracket_match.group(1),
                "sender": bracket_match.group(2).strip(),
                "content": bracket_match.group(3).strip(),
                "is_target": bracket_match.group(2).strip() == target,
            }
            continue

        # 格式: 发送者 时间\n 内容 (续行)
        if current_msg is not None:
            current_msg["content"] += line
        else:
            # 无法解析的行，跳过
            continue

    if current_msg:
        messages.append(current_msg)

    return messages


def analyze_particles(messages: list[dict]) -> list[tuple[str, int]]:
    """分析目标人物的语气词使用频率。"""
    counter = Counter()
    for msg in messages:
        if not msg["is_target"]:
            continue
        for pattern in PARTICLE_PATTERNS:
            matches = re.findall(pattern, msg["content"])
            for m in matches:
                counter[m] += 1
    return counter.most_common(10)


def analyze_emoji(messages: list[dict]) -> list[tuple[str, int]]:
    """分析目标人物的 emoji 使用频率。"""
    counter = Counter()
    for msg in messages:
        if not msg["is_target"]:
            continue
        emojis = EMOJI_PATTERN.findall(msg["content"])
        for e in emojis:
            counter[e] += 1
    return counter.most_common(10)


def analyze_punctuation(messages: list[dict]) -> dict:
    """分析目标人物的标点使用习惯。"""
    stats = {name: 0 for name in PUNCT_MAP}
    total_chars = 0

    for msg in messages:
        if not msg["is_target"]:
            continue
        total_chars += len(msg["content"])
        for pname, pattern in PUNCT_MAP.items():
            stats[pname] += len(re.findall(pattern, msg["content"]))

    if total_chars > 0:
        stats = {k: round(v / total_chars * 1000, 2) for k, v in stats.items()}

    return stats


def analyze_message_length(messages: list[dict]) -> dict:
    """分析目标人物的消息长度分布。"""
    lengths = [len(m["content"]) for m in messages if m["is_target"] and m["content"]]
    if not lengths:
        return {"average": 0, "style": "unknown", "short_ratio": 0}

    avg = sum(lengths) / len(lengths)
    short_count = sum(1 for l in lengths if l < 20)

    style = "short_burst" if avg < 20 else ("medium" if avg < 60 else "long_form")

    return {
        "average": round(avg, 1),
        "min": min(lengths),
        "max": max(lengths),
        "style": style,
        "short_ratio": round(short_count / len(lengths), 2),
    }


def extract_samples(messages: list[dict], limit: int = 50) -> list[str]:
    """提取目标人物的代表性消息样本。"""
    samples = []
    for msg in messages:
        if msg["is_target"] and msg["content"].strip():
            samples.append(msg["content"].strip())
            if len(samples) >= limit:
                break
    return samples


def analyze_messages(messages: list[dict]) -> dict:
    """综合分析并返回结构化结果。"""
    target_msgs = [m for m in messages if m["is_target"]]
    total_msgs = len(messages)
    target_count = len(target_msgs)

    return {
        "total_messages": total_msgs,
        "target_messages": target_count,
        "target_ratio": round(target_count / max(total_msgs, 1), 2),
        "particles": analyze_particles(messages),
        "emoji": analyze_emoji(messages),
        "punctuation": analyze_punctuation(messages),
        "message_length": analyze_message_length(messages),
        "samples": extract_samples(messages),
    }


def main():
    parser = argparse.ArgumentParser(description="WeChat Chat Log Parser")
    parser.add_argument("input_file", help="Path to exported WeChat chat log")
    parser.add_argument("--target", required=True, help="Target person's name")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    messages = parse_messages(text, args.target)

    if not messages:
        print("Error: No messages parsed. Check input format.", file=sys.stderr)
        sys.exit(1)

    result = analyze_messages(messages)
    result["source"] = str(input_path)
    result["target"] = args.target

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
