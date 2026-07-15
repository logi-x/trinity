---
title: "2026 06 10 event settlement refunds 1 review"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-10-event-settlement-refunds-1-review.md"
---
Spawned and closed all six requested reviewers. I also checked issue `#966`, the spec, app guidance, GitNexus context, and the relevant refund/settlement/event files. Issue `#966` matches the spec and adds no extra acceptance detail.

**Recommendation: No-go as written.** The plan is directionally good, but it is not yet a production-ready one-shot plan. There are several foot-guns that should be amended in the spec before execution.

**Must Fix Before Implementation**

- Event refund processing should set `EventRegistration.status = "refunded"`, not `cancelled`. The enum already has `refunded`, and event revenue stats only count refunded revenue for that status: [schema.prisma](/home/logix/experts/apps/experts-app/prisma/schema.prisma:2580), [event-list.handler.ts](/home/logix/experts/apps/experts-app/src/lib/events/handlers/event-list.handler.ts:292).
- Public/legal/AI policy conflicts with E-1. The spec says 7-day-from-registration capped at event start; current legal/AI copy says 48 hours before event start: [legal.json](/home/logix/experts/apps/experts-app/src/i18n/messages/en/legal.json:285), [ask-ai-assistant.ts](/home/logix/experts/apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts:75).
- Admin refund approve/reject/process routes must dispatch by `sourceType`; they currently call course handlers directly, and course handlers assume non-null `enrollmentId`: [process route](/home/logix/experts/apps/experts-app/app/api/v1/admin/refunds/[id]/process/route.ts:1), [course process handler](/home/logix/experts/apps/experts-app/src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts:21).
- Admin refund query/DTO/table need a discriminated mixed-source shape, not just a chip. Current query/DTO/table are course-shaped: [refund-request.query.ts](/home/logix/experts/apps/experts-app/src/lib/courses/enrollments/queries/refund-request.query.ts:16), [refund-request.dto.ts](/home/logix/experts/apps/experts-app/src/lib/courses/enrollments/dto/refund-request.dto.ts:1), [refunds-table.tsx](</home/logix/experts/apps/experts-app/app/(i18n)/_shared/admin/refunds/_components/refunds-table.tsx:106>).
- Event affiliate commission clawback is missing. Event purchases create affiliate attribution, but the shared helper only covers creator settlement clawback. Event refund processing must also cancel pending/approved event commissions keyed by buyer + `itemType:"event"` + `eventId`: [event-registration-complete.handler.ts](/home/logix/experts/apps/experts-app/src/lib/events/handlers/event-registration-complete.handler.ts:173), [course refund process](/home/logix/experts/apps/experts-app/src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts:206).
- Event affiliate hold timing conflicts with E-1. Current event affiliate hold is 3 days, while the refund window may remain open longer until event start: [affiliate.helper.ts](/home/logix/experts/apps/experts-app/src/lib/affiliate/helpers/affiliate.helper.ts:119).
- The spec references event fallback start/end fields that do not exist. Current timing lives in occurrences/schedules/slots; define exact behavior for cancelled occurrences, no occurrences, and fallback/skip rules: [schema.prisma](/home/logix/experts/apps/experts-app/prisma/schema.prisma:844).
- Event invoice correlation is under-specified. Event invoices persist `contentType/contentId`, not `occurrenceId`, and `contentId` is the event id while settlement source id is planned as registration id: [invoice-source.mapper.ts](/home/logix/experts/apps/experts-app/src/lib/billing/mappers/invoice-source.mapper.ts:1), [schema.prisma](/home/logix/experts/apps/experts-app/prisma/schema.prisma:1121).
- Add the inverse Prisma relation on `EventRegistration` for the new `RefundRequest.registration` relation, then require `pnpm db:generate` / Prisma validation in the sequence.
- Consider hardening credit-note idempotency. `CreditNote.invoiceId` is not unique and `RefundRequest` does not store a credit note link, so double-process races can create duplicate credit notes: [schema.prisma](/home/logix/experts/apps/experts-app/prisma/schema.prisma:1315).

**Enhancements Worth Adding To The Spec**

- Add an event-specific settlement rollout gate or explicit deploy order. Existing settlement is controlled only by `SETTLEMENT_LEDGER_ENABLED`, so adding events could start settling immediately if the flag is already on: [record-settlement.ts](/home/logix/experts/apps/experts-app/src/lib/settlement/record-settlement.ts:60).
- Make reconcile fair across course/subscription/event instead of always spending the budget in source order: [reconcile-settlements.ts](/home/logix/experts/apps/experts-app/src/lib/settlement/reconcile-settlements.ts:1).
- Move refund admin query/DTO out of the course module into a neutral billing/refund module.
- Add regression tests for existing course and subscription settlement behavior after widening `recordOrderSettlement`, not only event tests.
- Add concurrency tests for double process, credit-note race, payout-complete race, and reconcile-vs-refund race.

No files were edited and no tests were run; this was a read-only plan review.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
