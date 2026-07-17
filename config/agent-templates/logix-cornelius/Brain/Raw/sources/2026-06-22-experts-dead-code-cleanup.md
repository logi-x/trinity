---
title: "Experts Dead Code Cleanup"
date: "2026-06-22"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts verified dead-code cleanup

Date: 2026-06-22
Repository: `logi-x/experts`
Issue: `#1125`
Pull request: `#1127`
Branch: `codex/chore-gh-1125-cleanup-audit`

## What changed

- Removed five components with zero verified callers, including an exact event-detail duplicate and a superseded 626-line curriculum component.
- Removed a dead post-detail mapper, unused compatibility aliases, deprecated Redis helpers, unread realtime state, dead billing/ZATCA values, and a permanently unreachable dashboard branch.
- Removed nine direct dependencies with no verified runtime, build, test, or tooling usage.
- Net committed diff: 2,400 deleted lines and 1,028 inserted lines; most insertions are lockfile normalization.

## Verification

- GitNexus impact analysis ran before symbol edits.
- GitNexus change detection reported MEDIUM risk limited to existing pricing-page flows; no unexpected high-risk processes.
- Full suite passed: 435 files passed, 2 skipped; 3,223 tests passed, 14 skipped, 5 todo.
- Lint and typecheck passed.
- Repository formatting still fails only on three untouched baseline test files.

## Deferred constraints

- Knip findings are candidates, not proof; framework entry points, tests, scripts, dynamic imports, and barrel exports create false positives.
- Shared admin components have CRITICAL blast radius, so cosmetic unused-import edits were intentionally excluded.
- Payment, refund, enrollment, exam/quiz, and course/event clone groups must not be mechanically consolidated; their similarity may encode distinct business rules.
- The legacy `certifications-v1` route remains wired through locale routes and proxy configuration and is not dead code without a product migration decision.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
