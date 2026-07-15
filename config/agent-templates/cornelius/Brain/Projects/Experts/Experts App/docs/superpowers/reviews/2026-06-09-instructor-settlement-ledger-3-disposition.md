---
title: "2026 06 09 instructor settlement ledger 3 disposition"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-09-instructor-settlement-ledger-3-disposition.md"
---
# Round-3 disposition (#936)

8-lens pre-execution panel (workflow-orchestrator, concept-architect, code-reviewer, architecture-reviewer, product-manager, general-purpose fact-check, db-engineer, money-path security). Verdict going in: "close, not yet one-shot." All findings below are now folded into the spec + Plan A + Plan B, OR are operator decisions now made.

## Operator decisions (made this round)

- **Ship gating → off-by-default flag `SETTLEMENT_LEDGER_ENABLED`** (spec D-8). No dark-ledger window.
- **Events excluded from v1** (spec D-9). "Block until event clawback exists" + no event refund flow ⇒ courses-only v1; events ship later WITH their refund flow + clawback. Plan A is now **courses-only**; subscriptions (platform-only) stay in Plan B.

## Confirmed solid (no action)

- All round-1/2 fixes (B1–B9, I1–I5) correctly folded — code-reviewer, security, workflow, general-purpose.
- **Zero remaining factual errors** — general-purpose exhaustive symbol table: every model/field/path/import/table/insertion point EXISTS as named. The `discountInstructorCost` scare was checked and retracted (correct).
- B7 (Restrict), I4 (indexes), the view-SQL, two-PR seam — db-engineer confirmed sound.

## Folded fixes

| Tag          | Finding                                                                               | Where fixed                                                                     |
| ------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| R3-flag      | dark-ledger liability                                                                 | Plan A Phase 0 kill-switch; writer/cron no-op when off; Plan B go-live flips it |
| R3-scope     | event earnings un-clawback-able                                                       | Plan A courses-only; events deferred (spec §10/§13)                             |
| N1           | payout `processing` is a dead-end state                                               | Plan B Task 4.1 — transitions allowed from `{pending,processing}`               |
| missing-flow | refund clawback corrupts a linked pending payout                                      | Plan B Task 4.1b (new)                                                          |
| F1           | Plan B referenced non-existent `enqueueSettlement` (my inline-revision left it stale) | Plan B Task 2.3 → inline `recordOrderSettlement`                                |
| sec-HIGH     | commission re-query included `paid` → late-reconcile double-deduct                    | Plan A + B: `notIn:['cancelled','paid']`                                        |
| sec-HIGH     | payout amount from stale balance read                                                 | Plan B Task 3.3 — compute amount INSIDE the link tx from linked rows            |
| code-BLK     | `updateMany` can't filter by relation (maturation)                                    | Plan A Task 6.1 — two-step findMany→updateMany                                  |
| N4           | subscription status gate too narrow                                                   | Plan B Task 2.2 — gate on Invoice existence, not `status`                       |
| N3           | subscription inline failure had no sweep backstop                                     | Plan B Task 2.4 (new)                                                           |
| B8-test      | P2002 test built wrong error type                                                     | Plan A Task 3.1 — `new Prisma.PrismaClientKnownRequestError`                    |
| test         | reconciliation test mocked model methods vs `$queryRaw` impl                          | Plan A Task 5.1 — mocks `$queryRaw`                                             |
| F12/13       | event/clawback task source-vars + mocks underspecified                                | Plan A (event removed); clawback mock `orderSettlement.findUnique` added        |
| sec-CRIT     | stats route guard ambiguous                                                           | Plan A Task 5.3 — POST + CRON_SECRET, explicit                                  |
| sec-MED      | payout-method IBAN unbounded                                                          | Plan B Task 3.2 — zod regex/max + `@db.VarChar(34)`                             |
| sec-MED      | mirrored affiliate `details` debug leak                                               | Plan B Task 3.3 — explicitly NOT mirrored                                       |
| N5           | refund-after-paid platform loss invisible                                             | Plan A Task 7.1 — `platformLossAmount` observed                                 |
| DB-1         | partial-null shares silently → 100% primary                                           | Plan A Task 2.1 — resolver returns `usedFallback`, caller warns                 |
| DB-2         | view used `Decimal(12,2)` vs bare                                                     | Plan B — bare `@db.Decimal` (mirror AffiliateBalance)                           |
| DB-5         | zero-earning creator → null balance → 500                                             | Plan B — coalesce + test                                                        |
| DB-3         | ZATCA-immutability objection risk                                                     | Plan A — "internal ledger, not a ZATCA doc" comment                             |
| DB-8/9       | currency/iban widths                                                                  | Plan B — `VarChar(10)`/`VarChar(34)`                                            |
| arch-HIGH    | cron sidecar Docker wiring uncalled                                                   | Plan A final gate — deploy prereqs                                              |
| PM/threshold | 100 SAR magic literal                                                                 | `MINIMUM_CREATOR_PAYOUT_SAR` in settlement-config                               |
| arch-MED     | mocks hide schema drift                                                               | Plan A Task 3.1 — real-DB integration test                                      |
| sec-MED      | self-billing compliance gap at payout                                                 | spec §12 + Plan B operator gate (warn on `vatRegistered`)                       |

## Notes

- The product-manager and one general-purpose run reviewed from the **issue only** (couldn't read the docs — they're on branch `docs/gh-936-settlement-spec`, not the `main` working tree). Their doc-structure "blocking" claims (stub undesigned, clawback mis-sequenced) are already handled in the plans; their operator/scope points (dark ledger, threshold, event sign-off) are folded above.
- Subscription **renewal** behavior (new `Subscription` row per renewal?) remains an open verify-before-Plan-B item (spec §12).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
