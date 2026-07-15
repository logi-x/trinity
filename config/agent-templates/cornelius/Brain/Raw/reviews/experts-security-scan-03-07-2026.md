Code review: Experts monorepo — findings

I ran four parallel read-only reviews (money paths, events/enrollment, security/trust-boundaries, and business-logic edge cases) across apps/experts-app. The codebase is genuinely well-hardened — settlement/FX math, refund-window snapshotting, admin-route auth (all 69 /api/v1/admin/** routes gate correctly), and the upload pipeline are all solid. The real problems cluster in three places: user-supplied URL validation, the payment webhook trust boundary, and the certification state machine. I spot-verified the top two against source myself.

🔴 Critical

1. Stored XSS via certification evidence links — hits admins.
certification-submit.schema.ts:40-45 (and certification-resubmit.schema.ts) validate linkedinUrl/websiteUrl/proofOfExpertise[].url with bare z.string().url(), which accepts javascript: and data: schemes. These are stored verbatim and rendered as raw <a href={value}> in the admin certification-review queue (certifications-queue-client.tsx). Any authenticated user submits an application with websiteUrl: "javascript:fetch('/api/v1/admin/users')…"; when an admin clicks the link, it runs in their authenticated session — approve payouts, grant admin, take down content. Fix: use the existing ^https?:// regex primitive already in community/validation/post.schema.ts, at the schema and at render (to cover already-stored rows). This repo has fixed this exact z.url() class before but never propagated the fix into a shared primitive — hence the recurrence.

2. Revoking a superseded VERIFIED certification silently strips an active ACADEMIC one.
certification-revoke.handler.ts:37-50: the "does another approval still exist?" check runs only in the applicationType === "ACADEMIC" branch. When an admin revokes a VERIFIED application, newLevel stays null unconditionally, so the transaction sets currentLevel: null, certificateIssuanceEnabled: false even though the user still holds an APPROVED ACADEMIC application. Result: an admin correcting an old fraudulent VERIFIED submission silently disables a legitimate instructor's ACADEMIC-tier course publishing. The sibling certification-approve.handler.ts:47-59 has the mirror bug — approving VERIFIED while ACADEMIC is active unconditionally downgrades currentLevel. Fix: compute the new level as the max of all remaining APPROVED applications, not from the one being acted on. One open question worth your call: is currentLevel meant to be "highest currently-approved tier" (then this is a bug) or "last decision" (then it's by-design but the UX is dangerous)?

🟠 High

3. Tabby webhook verifies the signature over one body but parses another.
webhook.channel.ts:9-20 sets parseBody = bearerToken ?? rawBody and parses that, but tabby.provider.ts computes the HMAC over rawBody only. The bearer-token override exists for Noon's JWT variant but is applied to all providers. An attacker with any one valid (rawBody, signature) pair sends it plus an Authorization: Bearer {…attacker JSON…} header — verify() passes on the real body, parse() returns the attacker's JSON — letting them mark an arbitrary enrollment/registration "completed" (free access). Exploitability in strict production depends on obtaining one signature, but it defeats the HMAC entirely and should be fixed regardless. Fix: scope the bearer-token substitution per-provider so Tabby always parses exactly what it verified.

4. Noon webhook returns 401 for every error, so the PSP stops retrying.
app/api/webhooks/noon/route.ts:15-22 hardcodes status: 401 in the catch — for DB errors, parse failures, the idempotency race, everything. The sibling Tabby route deliberately returns 500 for non-signature errors with a comment explaining why (PSPs don't retry 401 but do retry 5xx). Noon's webhook is the sole trigger for completion, so a transient blip → 401 → Noon gives up → buyer paid but never enrolled, creator never settled, invisible until someone runs the stuck-checkout admin query. Fix: mirror Tabby — only 401 on signature failure.

5. Silent ?? 0 on provider-reported amount can permanently zero creator earnings.
noon.webhook.handler.ts:395,449 and tabby.webhook.handler.ts:369,454 do Number(event.amount ?? 0), feeding straight into amountPaid → settlement grossPaid. If a provider payload lacks the amount in the exact nested shape expected, amountPaid persists as 0 on a completed purchase. Three things make it permanent: settlement treats <= 0 as a free order (zero CreatorEarning), the reconciliation sweep excludes amount_paid > 0 so it's never retried, and the charge-mismatch alarm only fires for FX-converted purchases (lockedSar != null) — so SAR-native sales, the majority, have no cross-check. Buyer's invoice looks correct; creator is silently underpaid. Fix: verify the amount against the provider's order-lookup API instead of trusting the webhook field, and alarm on amountPaid == 0 for a completed paid order.

6. Deleting an event time slot orphans ticket offers, which are then silently dropped.
use-event-form.ts:621 (removeTimeSlot) filters timeSlots but never prunes the deleted slot id from TicketOfferForm.includedSlotIds. The validity check still sees a non-empty array (with a ghost id) and reports the offer valid; on save, sync-ticket-offers.ts:41-45 resolves the ghost to nothing, occurrenceIds becomes [], and the offer is filtered out with no error. A creator deletes day 3 of a 3-day event, sees no warning, saves — an offer tied to day 3 vanishes, and the event may silently revert its pricing mode. Untested. Fix: prune includedSlotIds in removeTimeSlot and surface a validation error for now-empty offers.

7. Course lesson/quiz/exam resource URLs — same z.url() XSS, student-facing.
Five schemas (course-lesson-create/update, course-quiz-create/update, course-exam) use unrestricted z.url(), rendered as <a href> in the student lesson player. Instructor → student cross-privilege XSS. Same regex fix as #1.

🟡 Medium

- OTP verification: no rate limit + missing ownership check. The three OTP-consume routes (verify-email/otp, phone/verify, phone/verify/confirowRateLimit — a 6-digit code (1M keyspace) is brute-forceable. Worse, phone/verify/confirm/route.ts:23-29 checks only if (!token) and nevertoken.userId === session.user.id (its email sibling does), so any authenticated user can brute-force any pending phone code and get their own account marked verified. Add the guard to all three and the ownership check to the phone confirm route. Severity rises to High if phoneVerifiedAt/emailVerifiedAt gate payout KYC or anti-fraud.
- Structural-cooldown gate keys on field presence, not value change. course-module-update.handler.ts:28-34 and course-lesson-bulk-update.handlon !== undefined / data.type !== undefined rather than diffing against the existing value (the sibling course-lesson-update.handler.ts does itcorrectly). A title-only edit that echoes back the unchanged position can 409-block on an active cooldown and consumes the week's structural-edit allowance.
- Free→paid update guard bypassable via API. event-update.handler.ts fires its guard only when !Array.isArray(body.ticketOffers), but sync/validation only runs inside if (scheduleData). A raw {isFree:false, price:100, ticketOffers:[…]} with no scheduleType skips both — a paid event with permanently unbuyable
0-price offers. Not reachable from the app's own form, but untested.
regorian dates use host-OS timezone. format-hijri-date.ts and the invoice PDF header call Intl.DateTimeFormat/toLocaleDateString without timeZone: "Asia/Riyadh". Only the production app container pins the TZ; an invoice rendered near midnight on any other host (couldn't confirm the PDF-worker image inherits the TZ) prints the wrong Saudi business date on a ZATCA-adjacent document.
- UI dead-end below 2 days with orphaned offers (event-schedule-section.tsx): if day count drops below 2 while stale offers exist, the mode-switch control unmounts but the "ticket options replace full pass" text still renders, with no reachable control to clear the offers.

🟢 Low / cleanup

- webhookEvent.create() idempotency is check-then-act; the losing side of a concurrent duplicate delivery throws an uncaught unique-constraint error (which, combined with #4, becomes a bad 401 to Noon). The refund path already handles this with a CAS pattern — mirror it.
- jwt.verify in noon.provider.ts:32 doesn't pass an explicit algorithms allowlist (not currently exploitable with jsonwebtoken@9, but defense-
- Empty 0-byte stub files refund-execute.command.ts / refund-execute.handler.ts under the money path — delete or fill; a reader could mistake them for the real refund-execute logic.
- Dead code: capacityRegisteredCount and the registeredCount i18n key (all consumers removed in b3069bf79); unwired post.liked/comment.mentionm if unshipped vs. regression before touching).

Suggested priority order: #1 and #2 (critical, both silently corrupt trust/data), then #3–#5 (payment integrity), then #6–#7. I did not edit anything — this is all read-only. Want me to open GitHub issues for the criticals/highs (via the beacon flow), or start fixing #1 and #2, which are the most clearly-wrong and self-contained?

---

All six reviewers are in and I've personally verified every Critical/High claim against the source. Here's the consolidated bug report.

---
Code review — Experts monorepo

I ran six parallel reviewers across billing/payments, auth/security, events, courses/content, the API route surface, and realtime/workers, then verified each high-severity finding against the actual code. The codebase is, on the whole, well-hardened — TOCTOU races in refunds/settlement, the access-grant model, admin-lock wiring, and rate-limit-before-hash ordering are all deliberately guarded with regression comments. The real problems cluster in two places: the event host authorization model and the recently-churned event ticketing/capacity code.

Findings I verified myself are marked ✓.

Critical

C1 — Event host privilege escalation (role-blind authorization). ✓
src/modules/permissions/permissions.service.ts:57-63, gate used at app/api/v1/events/[id]/hosts/route.ts:67-70 and [userId]/route.ts
isContentInstructor() returns true if any EventHost row exists — it never checks role. That function is the write-gate for adding/editing/deleting hosts, and the same any-role check gates event-update, event-delete, and event-clone handlers. A guest or speaker host can promote themselves to primary host, set their own revenueShare to 1.0, remove other hosts, or edit/delete/clone the event outright. The role column exists precisely to express this privilege boundary and is ignored.

C2 — Seats can be oversold; the capacity check is not atomic with the seat write. ✓
src/lib/events/handlers/event-register.handler.ts:202-225, src/lib/events/capacity/registration-capacity.ts:8
assertRegistrationCapacity runs in a $transaction that only reads counts (no SELECT … FOR UPDATE, default isolation, no seat-cap DB constraint). The upsert that actually consumes the seat happens in a separate statement afterward (and after a payment round-trip for paid tickets). Compounding it,
TAKEN_SPOT_STATUSES = ["completed"] (line 8, changed from ["pending","completed"] in 2d018e738) means an in-flight registration reserves nothist seat concurrently both read taken < capacity, both pass, both complete → oversold. This directly undermines the per-ticket seat-quotafeature shipped in 7f3d29931.

High

Credit notes and invoices share the same seq.generate_invoice_number() counter. invoice-create.handler.ts handles the documented "counter fell behind the table" desync with reconcileInvoiceSequence (GREATEST/MAX self-heal, 5 P2002 retries). The credit-note path has no equivalent — one creditNote.create inside the tx, no catch. Once the CRN counter desyncs (DB restore/reseed), the P2002 propagates uncaught to a 500, and since the counter is shared across all CRNs for the year, every subsequent 

refund fails identically until a human reconciles the sequence.

H3 — Removing a sold day from a multi-day event 500s the update endpoint. ✓
src/lib/events/handlers/event-update.handler.ts:678-681
The comment says the deleteMany "cascades their offer links / registrations" — but EventRegistration.occurrence is onDelete: Restrict (schema:1351; only EventTicketOfferOccurrence is Cascade at 1219). If a host removes a day that has a single_occurrence registration, Postgres raises an FK violation and PUT /api/v1/events/[id] fails uncaught with a raw 500 — no "this day has registrations" message.

H4 — Refund eligibility isn't scoped to the days actually purchased. ✓ (cross-confirmed by two reviewers)
event-registration-refund-request.handler.ts:84-93, event-registration-refund-process.handler.ts:54-84
The request handler special-cases only single_occurrence; a multi-day ticket_offer purchase falls through to resolveEventStart over all event days. The admin process handler is worse — it never even selects occurrence/ticketType, so it always evaluates against all days. A buyer of only day 5 who refunds while day 1 has started gets wrongly rejected (eventStarted), and the process handler can reject a refund the request handler already approved.

No throttle before consumeAuthToken, unlike login/register/access-code siblings. The unauthenticated email-OTP route is brute-forceable (1M codes, 60-min window) against a known email → email-verification takeover.

Medium (grouped)

- Event clone silently drops ticket offers and resets fullEventPassEnabled to the schema default true (event-clone.handler.ts:84,159-172) — cloned bundle event becomes a different pricing model with no warning.
- Event-detail private-content guard ignores pending registrations while the course equivalent honors them (event-detail.handler.ts:30-73 vs course-detail.handler.ts:32-46) — a buyer mid-checkout on a private event can get a 404.
- zod .url() accepts javascript:/data: URLs on certification submit fields rendered as admin <a href> (certification-submit.schema.ts); prod CSP blocks javascript: but data: top-level navigation (admin phishing) works everywhere, and staging's relaxed CSP re-opens the javascript: vector.
- PDF/ZATCA "completed" handlers use queue.getJob() (pdf-result.handler.ts:102, zatca-result.handler.ts:291) — the exact eviction race the AI handler documents as unsafe; under removeOnComplete load, invoice email/Slack/metadata can be skipped (reconciler eventually retries, so not permanent loss).
- aggregate-engagement.ts:26,60,142 builds its IN (…) via unescaped Prisma.raw — not exploitable through current callers (all validated UUIDs)er with zero defense-in-depth; one future raw-ID caller reintroduces SQL injection.
- Contact-form mail endpoint has no rate limit beyond Turnstile (internal/mail/send/route.ts) — replayed token → notification spam.
- WebSocket fan-out has no backpressure (experts-realtime/src/server.ts:342-349) — no bufferedAmount check; a slow client on a busy channel grows the send buffer unboundedly.
- Two N+1 hot paths: sequential per-instructor stat loop on course detail (course-detail.handler.ts:99-124) and unbatched getCapacitySnapshot on multi-day event detail (registration-capacity.ts:546-605).


Native Bearer tokens aren't revoked on suspend (30-day stateless HMAC, native-session.ts — low blast radius today, only wired to self-scoped profile route); handleWsMessage lacks a top-level try/catch (server.ts:566); noon webhook P2002 dedupe race is misreported as a 401 signature failure; commissionAmount skips round2 (masked by Decimal(10,2)); a dead divergent publishing.service.ts/permissions.service.ts state machine with zero importers; misleading "published…cannot be modified" error text; duplicate activityHelpers modules; notify() @throws docstring contradicts its allSettled behavior.

---
Top three to fix first: C1 (host authz — active privilege escalation), C2 (seat oversell — money + the feature just shipped), and H2 (a DB reseed silently arms platform-wide refund failure). H1/H5/H3 are all quick, localized fixes.

Want me to fix any of these? C1, H1, H3, and H5 are small, self-contained changes I can make and verify; C2 and H2 need a design choice (unique constraint + serializable vs. a reservation row for C2; a shared reconcileSequence helper for H2) that's worth a quick decision before I touch them.

✻ Cogitated for 10m 1s

✻ Claude resuming /loop wakeup (Jul 3 8:52am)

That was my scheduled wakeup firing — but all six reviewers already reported back and I delivered the consolidated report in my previous message. Nothing left to collect.

Quick recap of where things landed: 2 Critical, 6 High, ~8 Medium, and a cluster of Low/hygiene items, every Critical and High verified against source. The two that most warrant immediate attention are C1 (event-host role-blind authorization → privilege escalation) and C2 (non-atomic capacity check → seat oversell), with H2 (credit-note sequence desync → platform-wide refund breakage) as a latent landmine that fires on the next DB reseed.

No further agents are running and I'm not rescheduling. Standing by — say the word and I'll fix C1/H1/H3/H5 (small, localized) right away, or walk through the C2/H2 design choice first.
