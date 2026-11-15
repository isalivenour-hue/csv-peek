#!/usr/bin/env python3
"""csv-peek: quick column profile for a CSV file. Standard library only."""
import argparse
import csv
import statistics
import sys
from collections import Counter


def to_number(value):
    try:
        return float(value.replace(",", "")) if value.strip() else None
    except ValueError:
        return None


def profile(rows, header):
    """Return a list of per-column dicts."""
    out = []
    for i, name in enumerate(header):
        vals = [r[i] if i < len(r) else "" for r in rows]
        filled = [v.strip() for v in vals if v.strip()]
        nums = [n for n in (to_number(v) for v in filled) if n is not None]
        info = {"name": name, "rows": len(vals), "empty": len(vals) - len(filled),
                "unique": len(set(filled))}
        if filled and len(nums) == len(filled):
            info["type"] = "number"
            info.update(min=min(nums), max=max(nums), mean=statistics.fmean(nums),
                        median=statistics.median(nums))
        else:
            info["type"] = "text"
            info["top"] = Counter(filled).most_common(3)
        out.append(info)
    return out


def fmt(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def render(info):
    lines = ["%s (%s): %d rows, %d empty, %d unique" % (
        info["name"], info["type"], info["rows"], info["empty"], info["unique"])]
    if info["type"] == "number":
        lines.append("  min %s  max %s  mean %s  median %s" % (
            fmt(info["min"]), fmt(info["max"]), fmt(info["mean"]), fmt(info["median"])))
    elif info["top"]:
        lines.append("  top: " + ", ".join("%s (%d)" % t for t in info["top"]))
    return "\n".join(lines)


def read_csv(fh, delimiter=","):
    reader = csv.reader(fh, delimiter=delimiter)
    try:
        header = next(reader)
    except StopIteration:
        return [], []
    return header, list(reader)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Quick profile of a CSV file.")
    ap.add_argument("file", help="CSV path, or - for stdin")
    ap.add_argument("-d", "--delimiter", default=",")
    args = ap.parse_args(argv)
    fh = sys.stdin if args.file == "-" else open(args.file, newline="", encoding="utf-8-sig")
    header, rows = read_csv(fh, args.delimiter)
    if not header:
        print("empty file")
        return 1
    print("%d rows, %d columns\n" % (len(rows), len(header)))
    for info in profile(rows, header):
        print(render(info))
    return 0


if __name__ == "__main__":
    sys.exit(main())
