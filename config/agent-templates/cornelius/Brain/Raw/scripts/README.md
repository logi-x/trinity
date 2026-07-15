---
title: "Vault scripts"
date: "2026-07-01"
tags: ["scripts", "meta", "project/experts"]
category: "meta"
---

# Vault scripts

## check-vault-links.py — stale-link & orphan check

Scans every `.md` / `.canvas` file for wikilinks (`…`, `!…`) and
markdown links to vault files, and reports any whose target doesn't resolve to
a real file. Resolution mirrors Obsidian (full path **or** basename; aliases
`|`, headings `#`, blocks `^` stripped; escaped table pipes `\|` handled; code
fences / inline code ignored; `<placeholder>` links skipped).

```bash
# from the vault root
python3 Raw/scripts/check-vault-links.py            # dangling links only
python3 Raw/scripts/check-vault-links.py --orphans  # + notes with no inbound/outbound link
```

Exit code **1** if any dangling links exist, **0** if clean — so it can gate a
routine, CI step, or pre-commit hook. Run it after editing `index.md` / `Home.md`
or any hub note to catch drift (renamed/deleted targets) before it rots.

**Known dangling (not bugs, just not-yet-ingested):** most current hits are
`Projects/Experts/Experts App/rules/*` and `*/.planning/*` — Cursor rules /
GSD planning that live in the **code repo**, referenced from vault notes but
never copied in. Either ingest those pages or prune the links.
