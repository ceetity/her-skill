#!/usr/bin/env python3
"""
Social Media Content Parser — 社交媒体内容解析器

从社交媒体导出内容中提取表达风格和兴趣标签。

Usage:
    python social_parser.py <input_file_or_directory> [--output <output_file>]
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


def parse_posts(text: str) -> list[dict]:
    """
    解析社交媒体帖子。
    通用格式: 每条帖子用空行分隔，可能包含时间戳。
    """
    posts = []
    blocks = re.split(r"\n{2,}", text.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # 尝试提取时间
        time_match = re.match(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2})", block)

        post = {
            "time": time_match.group(1) if time_match else None,
            "content": block,
            "has_images": bool(re.search(r"\[图片\]|<img|\.jpg|\.png", block, re.IGNORECASE)),
            "has_links": bool(re.search(r"https?://", block)),
        }
        posts.append(post)

    return posts


def analyze_expression_style(posts: list[dict]) -> dict:
    """分析表达风格。"""
    all_text = " ".join(p["content"] for p in posts)
    lengths = [len(p["content"]) for p in posts]

    # 情感词检测（简化版）
    positive_words = ["开心", "喜欢", "爱", "好棒", "幸福", "美", "满足", "期待", "激动", "感动"]
    negative_words = ["烦", "讨厌", "难过", "累", "焦虑", "无聊", "生气", "郁闷", "崩溃", "压力"]

    positive_count = sum(all_text.count(w) for w in positive_words)
    negative_count = sum(all_text.count(w) for w in negative_words)

    # 话题标签提取
    hashtags = re.findall(r"#([^#\s]+)#?", all_text)

    # 表达特征
    has_emoji = bool(re.search(r"[\U0001F600-\U0001F64F]", all_text))
    avg_length = sum(lengths) / max(len(lengths), 1)

    return {
        "total_posts": len(posts),
        "average_length": round(avg_length, 1),
        "has_emoji": has_emoji,
        "sentiment_ratio": {
            "positive": positive_count,
            "negative": negative_count,
            "tendency": "positive" if positive_count > negative_count else "negative"
            if negative_count > positive_count
            else "neutral",
        },
        "hashtags": Counter(hashtags).most_common(10),
        "posting_frequency": _estimate_frequency(posts),
    }


def _estimate_frequency(posts: list[dict]) -> str:
    """估算发帖频率。"""
    timestamps = [p["time"] for p in posts if p["time"]]
    if len(timestamps) < 2:
        return "unknown"

    # 简化估算
    return f"{len(posts)} posts analyzed"


def main():
    parser = argparse.ArgumentParser(description="Social Media Content Parser")
    parser.add_argument("input", help="Input file or directory path")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Path not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if input_path.is_dir():
        files = list(input_path.glob("*.txt")) + list(input_path.glob("*.md"))
    else:
        files = [input_path]

    all_posts = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        all_posts.extend(parse_posts(text))

    if not all_posts:
        print("Error: No posts parsed.", file=sys.stderr)
        sys.exit(1)

    result = analyze_expression_style(all_posts)
    result["source_files"] = [str(f) for f in files]

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
