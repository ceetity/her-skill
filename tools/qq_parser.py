#!/usr/bin/env python3
"""
QQ Chat Log Parser — QQ聊天记录解析器

从导出的QQ聊天记录（.txt）中提取语言特征。

Usage:
    python qq_parser.py <input_file> --target <target_qq_number_or_name> [--output <output_file>]
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_qq_messages(text: str, target: str) -> list[dict]:
    """
    解析QQ导出的聊天记录。
    支持常见格式:
    - 2024/1/1 12:00:00 Name\n content
    - [12:00:00] Name: content
    """
    messages = []
    lines = text.strip().split("\n")
    current_msg = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 格式: 日期 时间 昵称(QQ号)
        header = re.match(
            r"(\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+([^\(（]+)",
            line,
        )
        if header:
            if current_msg:
                messages.append(current_msg)
            current_msg = {
                "time": header.group(1),
                "sender": header.group(2).strip(),
                "content": "",
                "is_target": target in header.group(2),
            }
            continue

        # 格式: [时间] 昵称: 内容
        bracket = re.match(r"\[([^\]]+)\]\s*([^:：]+)[：:]\s*(.+)", line)
        if bracket:
            if current_msg:
                messages.append(current_msg)
            current_msg = {
                "time": bracket.group(1),
                "sender": bracket.group(2).strip(),
                "content": bracket.group(3).strip(),
                "is_target": target in bracket.group(2),
            }
            continue

        if current_msg is not None:
            current_msg["content"] += line

    if current_msg:
        messages.append(current_msg)

    return messages


def main():
    parser = argparse.ArgumentParser(description="QQ Chat Log Parser")
    parser.add_argument("input_file", help="Path to exported QQ chat log")
    parser.add_argument("--target", required=True, help="Target person's QQ number or name")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    messages = parse_qq_messages(text, args.target)

    if not messages:
        print("Error: No messages parsed.", file=sys.stderr)
        sys.exit(1)

    # 复用 wechat_parser 的分析函数
    from wechat_parser import analyze_messages

    result = analyze_messages(messages)
    result["source"] = str(input_path)
    result["target"] = args.target
    result["platform"] = "QQ"

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
