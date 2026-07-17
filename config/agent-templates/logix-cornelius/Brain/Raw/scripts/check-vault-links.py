#!/usr/bin/env python3
"""Stale-link check for the brain vault.

Scans every Markdown (and Canvas) file for Obsidian wikilinks `[[target]]` /
embeds `![[target]]` and reports any whose target does not resolve to a real
file. Resolution mirrors Obsidian: a link resolves if the target matches a
real vault path (with or without extension) OR a unique/By-basename file.

Usage:
    python3 raw/scripts/check-vault-links.py [--orphans] [--vault DIR]

Exit code 1 if any dangling links are found (so it can gate a routine/hook);
0 if the vault is clean. `--orphans` additionally lists notes with no inbound
AND no outbound wikilink (graph islands).
"""
import os, re, sys, json, argparse

WIKILINK = re.compile(r'!?\[\[([^\]]+)\]\]')          # [[target|alias]] / ![[...]]
MDLINK   = re.compile(r'\]\(([^)]+\.(?:md|canvas|base))\)')  # [txt](path.md)
FENCE    = re.compile(r'```.*?```', re.DOTALL)        # fenced code blocks
INLINE   = re.compile(r'`[^`\n]*`')                   # inline code (never spans newlines)

def strip_code(txt):
    return INLINE.sub('', FENCE.sub('', txt))

EXCLUDE_DIRS = {'node_modules', 'dist', 'build', '.trash'}

def vault_files(vault):
    out = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs
                   if not d.startswith('.') and d not in EXCLUDE_DIRS]
        for fn in files:
            out.append(os.path.relpath(os.path.join(root, fn), vault))
    return out

def strip_target(raw):
    # drop alias (| or escaped \|), heading (#), block (^); keep path + extension
    t = raw.replace('\\|', '|').split('|', 1)[0].split('#', 1)[0].split('^', 1)[0]
    return t.strip().rstrip('\\').strip()

def build_index(files):
    by_path = set()           # full relpaths, with and without .md
    by_base = {}              # basename(no ext) -> count
    for f in files:
        by_path.add(f)
        stem, ext = os.path.splitext(f)
        if ext == '.md':
            by_path.add(stem)             # allow extensionless md path links
        base = os.path.basename(stem)
        by_base[base] = by_base.get(base, 0) + 1
        by_base[os.path.basename(f)] = by_base.get(os.path.basename(f), 0) + 1
    return by_path, by_base

def resolves(target, by_path, by_base):
    if not target or target.startswith(('http://', 'https://')):
        return True
    if '<' in target or '>' in target:     # template placeholder, e.g. <Project Name>
        return True
    t = target.strip().lstrip('./')
    if t in by_path:
        return True
    if t + '.md' in by_path:
        return True
    base = os.path.basename(t)
    if base in by_base:                    # Obsidian basename resolution
        return True
    if os.path.splitext(base)[0] in by_base:
        return True
    return False

def scan(vault, want_orphans):
    files = vault_files(vault)
    md = [f for f in files if f.endswith(('.md', '.canvas'))]
    by_path, by_base = build_index(files)

    dangling = []   # (source, target)
    has_out = {}    # source -> bool
    inbound = set() # resolved basenames that are linked to
    for f in md:
        txt = open(os.path.join(vault, f), encoding='utf-8', errors='ignore').read()
        targets = []
        if f.endswith('.canvas'):
            try:
                for n in json.loads(txt).get('nodes', []):
                    if n.get('type') == 'file' and n.get('file'):
                        targets.append(n['file'])
            except Exception:
                pass
        else:
            body = strip_code(txt)
            targets += [strip_target(m) for m in WIKILINK.findall(body)]
            targets += [strip_target(m) for m in MDLINK.findall(body)]
        targets = [t for t in targets if t]
        has_out[f] = bool(targets)
        for t in targets:
            if resolves(t, by_path, by_base):
                inbound.add(os.path.splitext(os.path.basename(t.strip().lstrip('./')))[0])
            else:
                dangling.append((f, t))

    orphans = []
    if want_orphans:
        for f in md:
            if not f.endswith('.md'):
                continue
            base = os.path.splitext(os.path.basename(f))[0]
            if not has_out.get(f) and base not in inbound:
                orphans.append(f)
    return dangling, orphans

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ap.add_argument('--orphans', action='store_true')
    a = ap.parse_args()

    dangling, orphans = scan(a.vault, a.orphans)

    if dangling:
        print(f"✗ {len(dangling)} dangling link(s):\n")
        cur = None
        for src, tgt in sorted(dangling):
            if src != cur:
                print(f"  {src}")
                cur = src
            print(f"      → [[{tgt}]]")
    else:
        print("✓ no dangling links")

    if a.orphans:
        print(f"\n{'✗' if orphans else '✓'} {len(orphans)} orphan note(s) (no inbound + no outbound wikilink)")
        for o in sorted(orphans):
            print(f"      {o}")

    sys.exit(1 if dangling else 0)

if __name__ == '__main__':
    main()
