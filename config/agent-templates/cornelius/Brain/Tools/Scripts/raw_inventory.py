#!/usr/bin/env python3
"""Inventory Raw/ without rewriting it.

Raw is allowed to contain legacy source records. This script reports what is
there and highlights files that may deserve processing or relocation.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "Raw"
SCRATCH_HINTS = re.compile(r"(daily|scratch|random|todo|to-do|note|notes)", re.I)
SUMMARY_HINTS = re.compile(r"(source|transcript|meeting|review|article|research|plan|guide|bug)", re.I)


def main() -> int:
    if not RAW.exists():
        print("Raw folder does not exist")
        return 1

    files = [path for path in RAW.rglob("*") if path.is_file()]
    by_top: Counter[str] = Counter()
    by_suffix: Counter[str] = Counter()
    candidates_for_inbox: list[Path] = []
    candidates_for_summary: list[Path] = []

    for path in files:
        rel = path.relative_to(RAW)
        top = rel.parts[0] if len(rel.parts) > 1 else "."
        by_top[top] += 1
        by_suffix[path.suffix.lower() or "(none)"] += 1

        name = path.name.lower()
        rel_text = str(rel).lower()
        if SCRATCH_HINTS.search(name) and "random" in rel_text:
            candidates_for_inbox.append(path)
        if path.suffix.lower() == ".md" and SUMMARY_HINTS.search(rel_text):
            candidates_for_summary.append(path)

    print("Raw inventory")
    print(f"files={len(files)}")
    print()
    print("By folder:")
    for folder, count in sorted(by_top.items()):
        print(f"- {folder}: {count}")

    print()
    print("By suffix:")
    for suffix, count in sorted(by_suffix.items()):
        print(f"- {suffix}: {count}")

    if candidates_for_summary:
        print()
        print("Likely summary candidates:")
        for path in candidates_for_summary[:30]:
            print(f"- {path.relative_to(ROOT)}")
        if len(candidates_for_summary) > 30:
            print(f"- ... {len(candidates_for_summary) - 30} more")

    if candidates_for_inbox:
        print()
        print("Possible Inbox candidates:")
        for path in candidates_for_inbox[:30]:
            print(f"- {path.relative_to(ROOT)}")
        if len(candidates_for_inbox) > 30:
            print(f"- ... {len(candidates_for_inbox) - 30} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

