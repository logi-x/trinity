Here's a validation pass on the 4 gatekeeper BLOCKs. I'm scoring each finding on technical merit, not just whether it was filed:

Attempt 1 (PR #448) — BLOCK valid (4/4 real)

┌─────┬───────────────────────────────────────┬──────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Finding │ Verdict │ Reasoning │
├─────┼───────────────────────────────────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1 │ Monolithic try/catch → ledger drift │ ✅ Real CRITICAL │ If promote() throws after file.update commits, release() zeros reserved without incrementing used. File is ready in DB + R2 but unaccounted. Janitor cannot repair (it only touches reserved, never reconciles used). │
│ │ │ │ Permanent drift. │
├─────┼───────────────────────────────────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2 │ CRON_SECRET fail-open │ ✅ Real CRITICAL │ if (!cronSecret || authHeader !== ...) then requireAdmin() is fail-open by composition. Zero-all-reservations endpoint must fail-closed on missing config. │
├─────┼───────────────────────────────────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 3 │ Decrement w/o floor → negative │ ✅ Real HIGH │ Conditional UPDATE used + reserved + incoming <= quota with negative reserved literally inflates headroom. Quota bypass under double-promote / janitor races. │
│ │ reserved │ │ │
├─────┼───────────────────────────────────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 4 │ Missing real-DB concurrency test │ ✅ Real (acceptance criteria │ Issue spec said "must hit real connection pool; mocks can't surface the race." │
│ │ │ explicit) │ │
└─────┴───────────────────────────────────────┴──────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Attempt 2 (PR #463) — BLOCK valid (6/6 real)

┌─────┬────────────────────────────────────────────────┬──────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Finding │ Verdict │ Reasoning │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1 │ promote WHERE reserved_bytes >= incoming │ ✅ Real CRITICAL │ This was an overcorrection to A1#3. Janitor zeros reserved → promote matches 0 rows → silent no-op. Now used never increments, file is ready. Same drift class as A1#1, different mechanism. │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2 │ Buffer-oversize early-return leaks reservation │ ✅ Real HIGH │ Defense-in-depth path returns 413 without releaseReservation. Reservation held for up to 15 min, blocks legit retries. │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 3 │ Backfill a."userId" column-name risk │ ✅ Real HIGH │ Prisma's @@map converts to snake_case by default; raw SQL must match physical names. Trivially verifiable but a runtime crash if wrong. │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 4 │ updated_at no DEFAULT NOW() │ ✅ Real MEDIUM │ Any non-Prisma INSERT path fails. Defensive but legitimate. │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 5 │ Single PrismaClient concurrency test │ ✅ Real HIGH │ One client + pool size > 1 doesn't guarantee parallel execution. Test could pass trivially. Two independent clients + barrier is the right design. │
├─────┼────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 6 │ Tombstone misses 5th caller │ ✅ Real HIGH │ community/posts/[id]/thumbnail/route.ts:92 is a documented caller. Stale comment is a future-trap. │
└─────┴────────────────────────────────────────────────┴──────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Attempt 3 (PR #466) — BLOCK valid (1/1 real, narrowly correct)

┌─────┬─────────────────────────────────────────┬────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Finding │ Verdict │ Reasoning │
├─────┼─────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1 │ Pre-R2 $transaction failure leaks │ ✅ Real │ Reservation taken → DB transaction (file.create + attachment.create) fails → outer catch rethrows with no release. Pre-R2 path has no R2 side-effect, so releasing IS correct (distinct from the "don't release on post-R2 DB errors" guidance). │
│ │ reservation │ CRITICAL │ Surgical, narrow finding — correctly scoped. │
└─────┴─────────────────────────────────────────┴────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Attempt 4 (PR #469) — BLOCK valid (4/4 real, one critical regression)

┌─────┬────────────────────────────────────────┬───────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Finding │ Verdict │ Reasoning │
├─────┼────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1 │ Stale-branch regresses │ ✅ Real │ This is a branch-hygiene catastrophe, not a logic bug. A4 was built off pre-EXP-100-fix main, so the merge reverts the country-spoof guard. Tabby KSA eligibility becomes spoofable via raw cf-ipcountry. Completely out-of-scope regression. │
│ │ CF_ORIGIN_SECRET trust │ CRITICAL │ Gatekeeper correctly refused. │
├─────┼────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2 │ file.size reserve vs buffer.byteLength │ ✅ Real HIGH │ Browser-reported File.size can diverge from materialized buffer (multipart parser quirks, Blob slicing). Two different sources of truth = ledger drift. Use one canonical count. │
│ │ persist │ │ │
├─────┼────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 3 │ Backfill ON CONFLICT SET = EXCLUDED │ ✅ Real HIGH │ If backfill runs after app switch, a live upload that already incremented used_bytes gets overwritten by the older aggregate snapshot. Sequencing issue: must run backfill before app switch, OR use GREATEST(existing, excluded), OR additive │
│ │ clobbers live │ │ merge. │
├─────┼────────────────────────────────────────┼───────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 4 │ Cleanup zeros whole bucket │ ✅ Real HIGH │ One reserved_bytes column + one updated_at cannot distinguish stale from active. Slow upload's reservation gets reaped mid-flight → second upload reserves → first eventually promotes → over-quota. Needs per-reservation rows to be airtight │
│ │ │ │ (this is also why EXP-80's original spec design has this weakness — arguably a spec-level issue worth filing). │
└─────┴────────────────────────────────────────┴───────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Verdict

All 12 distinct blocking findings across 4 attempts are technically legitimate. Zero false positives. The gatekeeper is doing its job — these aren't pedantic style nits, every one is a correctness/security defect that would land in production.

Failure pattern across attempts:

- A1 → A2: overcorrected (added a guard that created a new silent-noop bug)
- A2 → A3: narrow fix, missed an adjacent error path
- A3 → A4: branched from stale main, reintroduced an already-fixed security guard, plus three new defects

  The recurring theme is ledger ↔ reality drift at every error boundary. The reservation pattern has many boundaries (preflight → reserve → DB-row-create → R2-put → DB-status-flip → promote, plus janitor in parallel), and each is its own drift opportunity. Each attempt fixed one boundary but missed another.

  Recommendation if you go for attempt 5:

- Rebase onto current main first (non-negotiable after A4)
- Treat the reservation lifecycle as a state machine with explicit transitions; enumerate every failure point and decide release/keep/promote per failure
- Consider whether the per-user-aggregate-column design is even salvageable, or whether EXP-80 needs a spec revision to per-reservation rows (would also kill A4#4 by construction)
- Author the failure-mode table in the PR description so the reviewer can check coverage instead of discovering gaps
