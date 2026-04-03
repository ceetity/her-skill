#!/usr/bin/env python3
"""
Version Manager — 版本备份与回滚管理器

管理数字副本的版本历史，支持备份、回滚和查看版本列表。

Commands:
    backup <slug>               — 创建当前版本备份
    rollback <slug>             — 回滚到上一版本
    list <slug>                 — 查看版本历史
    cleanup <slug> [--keep N]   — 保留最近N个版本，删除其余
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
HERS_DIR = PROJECT_ROOT / "hers"
VERSIONS_DIR_NAME = ".versions"
MAX_VERSIONS = 10  # 默认最大保留版本数


def _versions_dir(slug: str) -> Path:
    """获取版本目录。"""
    return HERS_DIR / slug / VERSIONS_DIR_NAME


def _get_timestamp() -> str:
    """获取时间戳字符串。"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(slug: str, label: str = "") -> str:
    """创建版本备份。"""
    her_dir = HERS_DIR / slug
    if not her_dir.exists():
        print(f"Error: '{slug}' does not exist.", file=sys.stderr)
        sys.exit(1)

    v_dir = _versions_dir(slug)
    v_dir.mkdir(exist_ok=True)

    timestamp = _get_timestamp()
    version_name = f"v_{timestamp}"
    if label:
        version_name += f"_{label}"

    version_path = v_dir / version_name
    shutil.copytree(her_dir, version_path, ignore=shutil.ignore_patterns(VERSIONS_DIR_NAME))

    # 记录版本信息
    version_meta = {
        "version": version_name,
        "timestamp": datetime.now().isoformat(),
        "label": label,
        "files": [
            f.name for f in version_path.iterdir() if f.is_file()
        ],
    }
    (version_path / ".version_meta.json").write_text(
        json.dumps(version_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 更新 meta.json
    meta_path = her_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["updated_at"] = datetime.now().isoformat()
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # 清理旧版本
    cleanup(slug)

    print(f"Backup created: {version_name}")
    return version_name


def rollback(slug: str) -> None:
    """回滚到上一版本。"""
    her_dir = HERS_DIR / slug
    v_dir = _versions_dir(slug)

    if not v_dir.exists():
        print("Error: No backups found.", file=sys.stderr)
        sys.exit(1)

    versions = sorted(v_dir.iterdir(), reverse=True)
    versions = [v for v in versions if v.is_dir()]

    if not versions:
        print("Error: No backups found.", file=sys.stderr)
        sys.exit(1)

    # 先备份当前状态
    backup(slug, label="pre_rollback")

    # 找到最新的非 pre_rollback 版本
    target = None
    for v in versions:
        if "pre_rollback" not in v.name:
            target = v
            break

    if not target:
        print("Error: No valid rollback target found.", file=sys.stderr)
        sys.exit(1)

    # 删除当前文件（保留 .versions 目录）
    for item in her_dir.iterdir():
        if item.name != VERSIONS_DIR_NAME:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # 恢复版本文件
    for item in target.iterdir():
        if item.name == ".version_meta.json":
            continue
        if item.is_dir():
            shutil.copytree(item, her_dir / item.name)
        else:
            shutil.copy2(item, her_dir / item.name)

    print(f"Rolled back to: {target.name}")

    # 显示版本信息
    meta_path = target / ".version_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        print(f"  Label: {meta.get('label', 'N/A')}")
        print(f"  Created: {meta.get('timestamp', 'N/A')}")


def list_versions(slug: str) -> None:
    """列出所有版本。"""
    v_dir = _versions_dir(slug)
    if not v_dir.exists():
        print("No versions found.")
        return

    versions = sorted(v_dir.iterdir(), reverse=True)
    versions = [v for v in versions if v.is_dir()]

    if not versions:
        print("No versions found.")
        return

    print(f"Version history for '{slug}' ({len(versions)} versions):\n")
    for i, v in enumerate(versions):
        meta_path = v / ".version_meta.json"
        label = ""
        ts = ""
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            label = meta.get("label", "")
            ts = meta.get("timestamp", "")[:19]

        marker = "← current" if i == 0 else ""
        print(f"  {v.name:40s} | {ts:20s} | {label:20s} {marker}")


def cleanup(slug: str, keep: int = MAX_VERSIONS) -> None:
    """清理旧版本，只保留最近N个。"""
    v_dir = _versions_dir(slug)
    if not v_dir.exists():
        return

    versions = sorted(v_dir.iterdir(), reverse=True)
    versions = [v for v in versions if v.is_dir()]

    if len(versions) <= keep:
        return

    for old in versions[keep:]:
        shutil.rmtree(old)
        print(f"Cleaned up old version: {old.name}")


def main():
    parser = argparse.ArgumentParser(description="Version Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # backup
    bp = subparsers.add_parser("backup", help="Create a version backup")
    bp.add_argument("slug", help="Her slug")
    bp.add_argument("--label", default="", help="Backup label")

    # rollback
    rp = subparsers.add_parser("rollback", help="Rollback to previous version")
    rp.add_argument("slug", help="Her slug")

    # list
    lp = subparsers.add_parser("list", help="List version history")
    lp.add_argument("slug", help="Her slug")

    # cleanup
    cp = subparsers.add_parser("cleanup", help="Clean up old versions")
    cp.add_argument("slug", help="Her slug")
    cp.add_argument("--keep", type=int, default=MAX_VERSIONS, help="Number of versions to keep")

    args = parser.parse_args()

    if args.command == "backup":
        backup(args.slug, args.label)
    elif args.command == "rollback":
        rollback(args.slug)
    elif args.command == "list":
        list_versions(args.slug)
    elif args.command == "cleanup":
        cleanup(args.slug, args.keep)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
