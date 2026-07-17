---
title: "2026-06-07 Experts Agent Digest"
date: "2026-06-07"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-06-07-experts-agent-digest.md"
---

# Experts Agent Digest — 07 June 2026

**Window:** 2026-06-06T00:00:00Z → 2026-06-07T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 0 |
| Resolved since yesterday | 5 |
| In-flight fixes (In Review) | 0 |
| Merged PRs | 19 |
| Needs human attention | 4 |

---

## New Today

No new issues filed by routines today. The backlog sweep from 2026-06-06 (which resolved 33 issues) has further reduced scan surface. Zero R3 findings in this window.

---

## Repeated Pattern

From `Raw/agent-state/findings-index.md` — files/symbols appearing 3+ times in last 30 days:

| Pattern | Occurrences (30d) | State Today |
|---------|-------------------|-------------|
| `ask-ai-assistant.ts` | **4 issues** (EXP-223 open, EXP-232 open, EXP-239✓, EXP-252✓) | EXP-223 (prompt injection) + EXP-232 (history injection) still Backlog. Both have been open 7+ days. Repeated in 5 consecutive digests (05-31→06-06). |
| **Community moderation lock** | **4 issues** (EXP-295 open, EXP-296 open, EXP-297✓, EXP-300✓) | EXP-295 (DELETE bypass) had IMMEDIATE flag filed 2026-06-03 — 4 days unaddressed. EXP-296 (PUT TOCTOU) also open. Both repeated in 3 digests (06-03, 06-06, 06-07). |
| **Admin route requireAdmin gaps** | **4 issues** (EXP-887 area: dashboard/subscriptions) | **Fully resolved today**: `requireAdmin()` added to admin subscriptions route (PR #890) and unauthenticated admin dashboard routes (PR #887). Class closed. |
| **Tabby payment paths** | **5 issues** (EXP-129✓, EXP-305✓, EXP-307✓, EXP-308✓, EXP-309✓) | **All resolved**. EXP-305 (paid-but-not-enrolled void) shipped today via PR #881. Full Tabby payment security class now closed. |

---

## Resolved Since Yesterday

Issues whose Linear status flipped to Done in the 2026-06-06/07 window (5 total):

| Issue | Title | Closed By | FP |
|-------|-------|-----------|-----|
| [EXP-305](https://linear.app/experts/issue/EXP-305) | Tabby geo-block leaves paid-but-not-enrolled — no refund/void on verify-403 or webhook block | PR #881 | b4961bb859ea |
| [EXP-83](https://linear.app/experts/issue/EXP-83) | VALIDATE course_isfree_price_consistency constraint (EXP-73 follow-up) | PR #880 | 2b75b1305d16 |
| [EXP-262](https://linear.app/experts/issue/EXP-262) | No per-user WebSocket connection cap — authenticated Redis exhaustion DoS | PR #879 | b5781cc27ee7 |
| [EXP-203](https://linear.app/experts/issue/EXP-203) | Replace broad EXP-189 no-restricted-syntax suppressions with shared diagnostics pattern | PR #878 | n/a (code quality) |
| [EXP-283](https://linear.app/experts/issue/EXP-283) | Add Docker digest-update automation (Dependabot) | PR #877 | 2925412d3273 |

---

## In-Flight Fixes

No issues in `In Review` state as of query time. EXP-120 and EXP-133 (CRON timing-safe fail-open) were previously shown as `in-review` in the findings index — live Linear query returns no In Review issues, suggesting they may have moved to Done or another state outside query visibility. **Verify live before closing.**

---

## Merged PRs

19 PRs merged to `main` in this window. Grouped by domain:

### Admin / UI — Orbit Kit Wave 2

| PR | Title |
|----|-------|
| [#874](https://github.com/logi-x/experts/pull/874) | feat(admin/kit): reusable admin design-system primitives |
| [#875](https://github.com/logi-x/experts/pull/875) | feat(admin/dashboard): rebuild on kit — hero KPIs + operations triage |
| [#876](https://github.com/logi-x/experts/pull/876) | feat(admin): ⌘K command palette |
| [#885](https://github.com/logi-x/experts/pull/885) | feat(admin): redesign Storage page on Orbit kit + i18n (Wave 2 / Operations) |
| [#888](https://github.com/logi-x/experts/pull/888) | Feat/admin orbit cleanup |
| [#889](https://github.com/logi-x/experts/pull/889) | docs(skills): add experts-textbook enhancement playbook |
| [#891](https://github.com/logi-x/experts/pull/891) | feat(admin): redesign Certifications page on Orbit kit (Wave 2 / Operations) |
| [#892](https://github.com/logi-x/experts/pull/892) | refactor(hooks): enhance useNowMs for improved time management |

### Security Fixes

| PR | Title | Issues |
|----|-------|--------|
| [#881](https://github.com/logi-x/experts/pull/881) | fix(payments): enforce Tabby geo-block before capture, void instead of capture | EXP-305 |
| [#887](https://github.com/logi-x/experts/pull/887) | fix(security): add requireAdmin guard to unauthenticated admin dashboard routes | — |
| [#890](https://github.com/logi-x/experts/pull/890) | fix(security): add requireAdmin guard to admin subscriptions route | — |

### Bug Fixes

| PR | Title | Issues |
|----|-------|--------|
| [#878](https://github.com/logi-x/experts/pull/878) | fix(ai): shared extractDiagnosticMessage helper, drop broad lint suppressions | EXP-203 |
| [#879](https://github.com/logi-x/experts/pull/879) | fix(realtime): per-user WebSocket connection cap + shorter token TTL | EXP-262 |
| [#880](https://github.com/logi-x/experts/pull/880) | fix(db): VALIDATE course_isfree_price_consistency constraint | EXP-83 |
| [#883](https://github.com/logi-x/experts/pull/883) | fix(deps): remediate Dependabot security findings (postcss, @hono/node-server, uuid) | — |

### CI / DevOps

| PR | Title |
|----|-------|
| [#877](https://github.com/logi-x/experts/pull/877) | chore(ci): Dependabot Docker digest-update automation (EXP-283) |
| [#882](https://github.com/logi-x/experts/pull/882) | chore(ci): extend Dependabot to npm + enable security updates |
| [#884](https://github.com/logi-x/experts/pull/884) | chore(ci): group Dependabot security updates per ecosystem/dir |

### Tooling

| PR | Title |
|----|-------|
| commit `03c00128` | fix(gitnexus): clarify analyze hook behavior to prevent KuzuDB corruption on timeout |

---

## Migrations / Env / Infra Changes

| Type | Path | PR | Notes |
|------|------|----|-------|
| Migration | `prisma/migrations/20260606000000_validate_course_isfree_price_consistency/migration.sql` | #880 | `VALIDATE CONSTRAINT course_isfree_price_consistency` — previously deferred pending prod data sweep confirming no `{is_free=true, price>0}` rows. Operator-confirmed and shipped. |
| CI config | `.github/dependabot.yml` | #882, #884 | Extended Dependabot coverage to npm packages; security-update PRs enabled; updates grouped by ecosystem/directory to reduce PR noise. Already covered Docker (PR #877). |
| Lock files | `apps/experts-app/pnpm-lock.yaml`, `apps/experts-prisma/pnpm-lock.yaml` | #883 | Security remediations: postcss, @hono/node-server, uuid. |

No Docker Compose, Dockerfile, Traefik, or `.env` changes in this window.

---

## Architectural Notes

Three items flagged for architectural significance:

**1. Admin Orbit Kit — Wave 2 complete.** PRs #874–#891 deliver the full kit + dashboard + ⌘K + Storage + Certifications redesign. The admin surface is now a coherent design system (primitives → page chrome → feature pages) rather than ad-hoc per-page components. This is a meaningful domain boundary win: admin UI is now kit-owned, not feature-owned. Decision-Log row not warranted — this is execution of the existing Admin Orbit programme.

**2. requireAdmin() hardening — class closure pattern.** PRs #887 and #890 add `requireAdmin()` to the admin subscriptions route and unauthenticated dashboard routes. Combined with the EXP-293 lint rule (auth-before-try) this represents a **structural fix pattern**: identify the class via lint/audit → fix all instances in a sweep. Worth noting: the `proxy.ts` page guard does NOT cover `/api/v1/admin/**` routes — each route requires an explicit `requireAdmin()` call. This invariant should be enforced by a lint rule if not already gated.

**3. Tabby payment flow reorder.** PR #881 moves the geo-block check *before* `captureTabbyPayment` and adds a void on 403. This changes the payment execution order — an irreversible monetary action (capture) is now guarded by an eligibility gate. Financially significant; correctly sequenced. The paid-but-not-enrolled remediation path (refund vs void) was also decided by the operator (void on geo-403 webhook block). No new architectural risk introduced; this closes the risk surface opened by EXP-305.

---

## Docs That Need Updating

| Doc / Skill | Trigger | Action |
|-------------|---------|--------|
| `apps/experts-app/.claude/skills/experts-orbit/SKILL.md` | Admin kit, ⌘K, and Wave 2 pages are now shipped. Orbit skill may reference planned rather than delivered components. | Verify skill reflects current shipped state; update component list if needed. |
| `apps/experts-app/CLAUDE.md` | `requireAdmin()` lint rule for `/api/v1/admin/**` routes — is this captured in CLAUDE.md or eslint config? | Confirm `no-auth-before-try` rule covers admin routes; document the invariant if not already in CLAUDE.md. |
| `~/brain/Action-Tracker.md` | EXP-283, EXP-262, EXP-203, EXP-83, EXP-305 rows marked "Open" → now Done. | Manually mark those rows Closed (Done #877–#881 respectively). Already partially done in the 2026-06-06 close-out section; verify no duplicates remain "Open". |

---

## Still Open

Agent-filed issues not yet In Review or Done (excluding design-blocked items):

| Issue | Title | Severity | Days Open | Notes |
|-------|-------|----------|-----------|-------|
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe compare fail-open on undefined | High | 18 | Was `in-review` per findings index; verify live state |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe compare fail-open on undefined | High | 18 | Same as above |
| [EXP-223](https://linear.app/experts/issue/EXP-223) | AI ask: prompt injection via unvalidated user history | Medium | 8 | Backlog; 5th consecutive digest |
| [EXP-232](https://linear.app/experts/issue/EXP-232) | AI ask: client-supplied history injected verbatim on conversationId | Medium | 8 | Backlog; 5th consecutive digest |
| [EXP-233](https://linear.app/experts/issue/EXP-233) | Quiz DELETE uses global isInstructor without course-ownership check (BOLA) | High | 8 | Backlog |
| [EXP-241](https://linear.app/experts/issue/EXP-241) | Community posts PUT uses JWT-derived isAdmin — revoked admin edits/pins any post | High | 8 | Backlog; 5th consecutive digest |
| [EXP-292](https://linear.app/experts/issue/EXP-292) | Course create auto-approves (design decision, EXP-226 dupe closed) | Design | — | Intentional; TODO(EXP-292) at course-create.handler.ts:98 |
| [EXP-293](https://linear.app/experts/issue/EXP-293) | auth()/getUserPermissions() before try — 37-handler class + lint rule | Medium | 4 | Was In Review per 06-06 digest; no In Review found in query today |
| [EXP-294](https://linear.app/experts/issue/EXP-294) | Community comment & post author email exposed (PII) | Medium | 4 | Backlog |
| [EXP-295](https://linear.app/experts/issue/EXP-295) | Owner can delete admin-locked post — moderation lock not enforced in DELETE | High | 4 | **IMMEDIATE** flag from 06-03; 4 days unaddressed |
| [EXP-296](https://linear.app/experts/issue/EXP-296) | TOCTOU race in PUT /posts/[id] allows non-admin to bypass moderation lock | Medium | 4 | Backlog |
| [EXP-319](https://linear.app/experts/issue/EXP-319) | AI cost controls: no kill-switch, no query-embed cache, cron/worker double-embed | High | 3 | PARTIAL: kill-switch (control 1) merged #838/#839; controls 2–5 open |
| [EXP-320](https://linear.app/experts/issue/EXP-320) | Functional-Impact gate: scanner fixes break happy-paths (process issue) | High | 3 | Blocked on R5 gatekeeper adding the gate |

---

## Needs Human Attention

Items appearing in 3+ consecutive digests that are still open or in-review:

| Issue | Title | Severity | Digest Count | Status | Recommended Action |
|-------|-------|----------|--------------|--------|--------------------|
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe fail-open | High | **6+ digests** (since 05-31) | Possibly in-review | Verify live Linear state — if still open, prioritise immediately; any request reaches CRON routes without a secret. |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe fail-open | High | **6+ digests** (since 05-31) | Possibly in-review | Same as EXP-120 — paired issues, fix together. |
| [EXP-232](https://linear.app/experts/issue/EXP-232) | AI ask: verbatim client history injection | Medium | **5 digests** (05-31→06-07) | Backlog | Client-controlled assistant turns enable prompt injection. Needs a decision: strip untrusted turns server-side or move to server-reconstructed history. |
| [EXP-295](https://linear.app/experts/issue/EXP-295) | Community DELETE moderation-lock bypass | High | **3 digests** (06-03, 06-06, 06-07) | Backlog | Filed as **IMMEDIATE** 2026-06-03. Owner can delete admin-locked post; 15-line fix. 4 days unaddressed — escalate. |

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
