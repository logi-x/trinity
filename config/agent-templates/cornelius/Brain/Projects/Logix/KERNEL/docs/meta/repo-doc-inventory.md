---
title: "Repo Doc Inventory"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "docs/meta"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Repo Doc Inventory

Material under `` `/home/logix/logix-kernel/docs/` `` that is **intentionally not** copied into the vault. Use the repo when executing plans; use [[Projects/Logix/KERNEL/docs|curated docs]] for stable architecture and operations.

| Area | Repo paths | Why vault skips |
| ---- | ---------- | ---------------- |
| **Implementation plans** | `docs/plans/*.md` (including large `phase-1.md` agent prompt, dated `2026-07-*` plans) | Living checklists; duplicate phase summaries; high churn |
| **Superpowers** | `docs/superpowers/specs/`, `docs/superpowers/plans/` | Session-scoped design/plan artifacts |
| **Audit** | `docs/audit/` | Point-in-time reports |
| **CLI depth** | `docs/cli/*.md` except overview (summarized in [[Projects/Logix/KERNEL/docs/guides/cli|CLI guide]]) | Tied to CLI help strings and slice work |
| **Product tour** | `docs/product/phase-1-tour.md` | Condensed into [[Projects/Logix/KERNEL/docs/reference/product-phase-1-surface|Phase 1 surface]] |

## Quick repo lookup

```text
docs/architecture/     → mirrored in reference/*
docs/adr/              → mirrored in decisions/*
docs/plans/            → roadmap summary only; full text in repo
docs/cli/              → guides/cli + repo
docs/superpowers/      → repo only
docs/audit/            → repo only
```

When filing vault notes from kernel work, tag `project/logix-kernel` and link `up:` to [[Entities/Projects/Logix Kernel]] or [[Projects/Logix/KERNEL/docs]].
