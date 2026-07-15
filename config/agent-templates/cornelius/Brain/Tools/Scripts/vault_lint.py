#!/usr/bin/env python3
"""Brain v2 vault lint.

This script intentionally uses only the Python standard library so it can run in
fresh agent environments.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAINTAINED_DIRS = {
    "Actions",
    "Agents",
    "Decisions",
    "Entities",
    "Inbox",
    "Projects",
    "Tools",
    "Wiki",
}
IGNORED_DIRS = {".git", ".obsidian", ".cursor", ".claude"}
TEXT_SUFFIXES = {".md", ".base", ".canvas", ".txt", ".yml", ".yaml", ".json"}
FRESHNESS_LEVELS = {"stable", "slow", "volatile", "live"}
FRESHNESS_REQUIRED = [
    "Entities/Projects/Experts App.md",
    "Entities/Projects/Experts.md",
    "Entities/Projects/Experts OS.md",
    "Entities/Projects/Logix Kernel.md",
    "Actions/Action-Tracker.md",
    "Decisions/Decision-Log.md",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def iter_markdown() -> list[Path]:
    return [path for path in iter_files() if path.suffix.lower() == ".md"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "", text)


def frontmatter_block(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return ""
    return match.group(1)


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


def check_frontmatter(markdown_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in markdown_files:
        top = path.relative_to(ROOT).parts[0]
        if top not in MAINTAINED_DIRS:
            continue
        text = read_text(path)
        fm = frontmatter_block(text)
        if fm is None:
            errors.append(f"missing frontmatter: {rel(path)}")
            continue
        if fm == "":
            errors.append(f"unterminated frontmatter: {rel(path)}")
            continue
        for key in ("title", "date", "updated", "tags", "category"):
            if not re.search(rf"(?m)^{re.escape(key)}\s*:", fm):
                errors.append(f"frontmatter missing {key}: {rel(path)}")
    return errors


def build_link_targets(files: list[Path]) -> set[str]:
    targets: set[str] = set()
    for path in files:
        path_rel = rel(path)
        no_ext = rel(path.with_suffix(""))
        targets.update({path_rel, no_ext, path.name, path.stem})
    return targets


def check_wikilinks(markdown_files: list[Path], targets: set[str]) -> list[str]:
    errors: list[str] = []
    for path in markdown_files:
        text = strip_code(read_text(path))
        for match in re.finditer(r"\[\[([^\]|#]+)", text):
            target = match.group(1).strip().replace("\\", "")
            if target and target not in targets:
                errors.append(f"broken wikilink in {rel(path)}: [[{target}]]")
    return errors


def check_v1_paths(files: list[Path]) -> list[str]:
    errors: list[str] = []
    scoped = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "index.md",
        ROOT / "Wiki" / "Concepts" / "CRITICAL_FACTS.md",
    ]
    scoped += [path for path in files if path.suffix.lower() in {".base", ".canvas"}]
    patterns = [
        "Entities/Topics/",
        "[[Entities/Topics",
        "file.inFolder(\"raw/",
        "file.inFolder('raw/",
        "file.folder == \"raw/",
        "file.folder == 'raw/",
    ]
    for path in scoped:
        if not path.exists():
            continue
        text = read_text(path)
        for pattern in patterns:
            if pattern in text:
                errors.append(f"v1 path reference in {rel(path)}: {pattern}")
    return errors


def check_placement() -> list[str]:
    errors: list[str] = []
    topics = ROOT / "Entities" / "Topics"
    if topics.exists():
        errors.append("misplaced folder exists: Entities/Topics should be Wiki/Concepts")
    raw_lower = ROOT / "raw"
    if raw_lower.exists():
        errors.append("misplaced folder exists: raw should be Raw")
    return errors


def check_summaries() -> list[str]:
    errors: list[str] = []
    summaries = ROOT / "Wiki" / "Summaries"
    if summaries.exists():
        for path in summaries.glob("*.md"):
            if path.name in {"Summaries.md", "README.md"}:
                continue
            if not path.name.startswith("S - "):
                errors.append(f"summary missing S - prefix: {rel(path)}")
    return errors


def check_raw_daily_notes(markdown_files: list[Path]) -> list[str]:
    errors: list[str] = []
    daily_pattern = re.compile(r"(^|[-_ ])daily([-_ ]|$)|\bjournal\b", re.I)
    for path in markdown_files:
        parts = path.relative_to(ROOT).parts
        if not parts or parts[0] != "Raw":
            continue
        if daily_pattern.search(path.stem):
            errors.append(f"daily/scratch-looking note in Raw; use Inbox: {rel(path)}")
    return errors


def check_freshness_metadata() -> list[str]:
    errors: list[str] = []
    required_keys = ("freshness", "verified", "source_of_truth", "verify_with")
    for relative in FRESHNESS_REQUIRED:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"freshness required page missing: {relative}")
            continue
        fm = frontmatter_block(read_text(path))
        if not fm:
            errors.append(f"freshness page missing frontmatter: {relative}")
            continue
        for key in required_keys:
            if not re.search(rf"(?m)^{re.escape(key)}\s*:", fm):
                errors.append(f"freshness metadata missing {key}: {relative}")
        freshness = frontmatter_value(fm, "freshness")
        if freshness and freshness not in FRESHNESS_LEVELS:
            errors.append(f"invalid freshness level in {relative}: {freshness}")
        if freshness in {"volatile", "live"}:
            source = frontmatter_value(fm, "source_of_truth")
            if not source:
                errors.append(f"volatile/live page missing source_of_truth value: {relative}")
            if re.search(r"(?m)^verify_with\s*:\s*$", fm) and not re.search(
                r"(?m)^verify_with\s*:\s*\n\s+-\s+", fm
            ):
                errors.append(f"volatile/live page has empty verify_with list: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the brain-v2 vault")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    files = iter_files()
    markdown_files = iter_markdown()
    targets = build_link_targets(files)

    errors: list[str] = []
    errors.extend(check_frontmatter(markdown_files))
    errors.extend(check_wikilinks(markdown_files, targets))
    errors.extend(check_v1_paths(files))
    errors.extend(check_placement())
    errors.extend(check_summaries())
    errors.extend(check_raw_daily_notes(markdown_files))
    errors.extend(check_freshness_metadata())

    if errors:
        print(f"vault_lint: FAIL ({len(errors)} issues)")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.quiet:
        print("vault_lint: OK")
        print(f"markdown_files={len(markdown_files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
