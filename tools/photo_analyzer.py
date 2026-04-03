#!/usr/bin/env python3
"""
Photo EXIF Analyzer — 照片EXIF信息提取器

从照片的EXIF数据中提取时间和地点信息，用于重建共同足迹。

Usage:
    python photo_analyzer.py <photo_or_directory> [--output <output_file>]
"""

import argparse
import json
import sys
from pathlib import Path


def extract_exif(photo_path: Path) -> dict | None:
    """从照片中提取EXIF信息。"""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS

        img = Image.open(photo_path)
        exif_data = img._getexif()
        if not exif_data:
            return None

        result = {
            "file": str(photo_path),
            "datetime": None,
            "gps": None,
            "camera": None,
        }

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTimeOriginal":
                result["datetime"] = str(value)
            elif tag == "DateTime":
                result["datetime"] = result["datetime"] or str(value)
            elif tag == "Model":
                result["camera"] = str(value)
            elif tag == "GPSInfo":
                gps = {}
                for gps_tag_id in value:
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps[gps_tag] = value[gps_tag_id]
                result["gps"] = _convert_gps(gps)

        return result

    except ImportError:
        print("Warning: Pillow not installed. Install with: pip install Pillow", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Warning: Could not read {photo_path}: {e}", file=sys.stderr)
        return None


def _convert_gps(gps: dict) -> dict | None:
    """将GPS坐标转换为十进制度数。"""
    try:
        lat_d = gps.get("GPSLatitude")
        lat_r = gps.get("GPSLatitudeRef")
        lon_d = gps.get("GPSLongitude")
        lon_r = gps.get("GPSLongitudeRef")

        if not lat_d or not lon_d:
            return None

        lat = _to_degrees(lat_d)
        lon = _to_degrees(lon_d)

        if lat_r == "S":
            lat = -lat
        if lon_r == "W":
            lon = -lon

        return {"latitude": round(lat, 6), "longitude": round(lon, 6)}
    except Exception:
        return None


def _to_degrees(values: tuple) -> float:
    """将GPS度分秒转换为十进制度数。"""
    d, m, s = values
    return float(d) + float(m) / 60.0 + float(s) / 3600.0


def analyze_photos(path: Path) -> list[dict]:
    """分析照片文件，提取EXIF信息。"""
    results = []

    if path.is_file():
        if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".tiff", ".heic"):
            exif = extract_exif(path)
            if exif:
                results.append(exif)
    elif path.is_dir():
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.tiff", "*.heic"):
            for photo in path.rglob(ext):
                exif = extract_exif(photo)
                if exif:
                    results.append(exif)

    # 按时间排序
    results.sort(key=lambda x: x.get("datetime") or "")

    return results


def build_footprint_timeline(exif_list: list[dict]) -> list[dict]:
    """从EXIF数据构建足迹时间线。"""
    timeline = []
    for item in exif_list:
        entry = {"file": item["file"]}
        if item.get("datetime"):
            entry["datetime"] = item["datetime"]
        if item.get("gps"):
            entry["gps"] = item["gps"]
        if entry.get("datetime") or entry.get("gps"):
            timeline.append(entry)
    return timeline


def main():
    parser = argparse.ArgumentParser(description="Photo EXIF Analyzer")
    parser.add_argument("input", help="Photo file or directory path")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Path not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    results = analyze_photos(input_path)

    if not results:
        print("No EXIF data found in provided photos.", file=sys.stderr)
        sys.exit(1)

    output_data = {
        "total_photos_analyzed": len(results),
        "photos_with_exif": len([r for r in results if r.get("datetime") or r.get("gps")]),
        "footprint_timeline": build_footprint_timeline(results),
        "details": results,
    }

    output = json.dumps(output_data, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Analysis saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
