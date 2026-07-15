---
title: "issue fix"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/designs/issue-fix.md"
---
🔍 What’s REALLY happening (root cause)
1️⃣ Ctrl + Shift + R ≠ normal refresh

When you hard-reload:

Next.js kills and restarts the Node runtime

Route handlers are re-imported

Fonts are re-registered

React-PDF’s internal global font store is reused but partially reset

@react-pdf/renderer is not HMR-safe and not reload-safe.

So what you get is:

A font object exists
but its internal glyph map / font id does NOT

Which leads directly to:

Cannot read properties of undefined (reading 'id')
at textkit.js

That’s why:

Invoice 1 works, 3 fails

Refresh flips behavior

Removing fontFamily “fixes” it

Happens only on hard reload

Happens only in API route rendering

This is expected behavior with React-PDF in server routes.

🚫 What NOT to do (important)

❌ Don’t render PDFs inside:

API routes during development

HMR cycles

Request/response loops you expect to hot-reload

❌ Don’t rely on React-PDF to behave like HTML/JSX
It is not React DOM — it’s a static layout engine.

✅ The Correct Architecture (production-grade)
Rule #1

React-PDF is a build artifact generator, not a live renderer

🧱 Recommended Design (Best Practice)
Split invoice rendering into 3 layers
① Invoice DATA → Pure JSON (shared)
// billing/invoice/invoice-view-model.ts
export type InvoiceViewModel = {
invoiceNumber: string;
issuedAt: string;
seller: {...};
buyer: {...};
lines: {...}[];
totals: {...};
branding: {...};
locale: "ar" | "en";
};

This is:

Used by HTML preview

Used by PDF generator

Used by tests

② HTML Invoice (HMR-safe, dev-first)

THIS is what you should view during development

// app/invoices/[id]/preview/page.tsx
import { InvoiceHtml } from "@/modules/billing/invoice/invoice-html";

export default function InvoicePreviewPage() {
return <InvoiceHtml {...invoiceData} />;
}

✔ Fast
✔ HMR-safe
✔ Fonts, SVGs, RTL all work
✔ Zero crashes

You iterate here 90% of the time.

③ PDF generation (isolated, cold-only)
Move PDF rendering to a non-HMR execution context
Option A (BEST): background worker / job
queue.add("generate-invoice-pdf", { invoiceId })

Worker:

const buffer = await renderToBuffer(<InvoicePdf {...data} />);

Option B (acceptable): API route but with guard
if (process.env.NODE_ENV === "development") {
throw new Error("PDF rendering disabled in dev. Use /preview.");
}

🛡️ Mandatory PDF Safety Guards (DO THESE)
1️⃣ Font registration must be singleton
// pdf/fonts/register.ts
let registered = false;

export function registerPdfFonts() {
if (registered) return;
registered = true;

Font.register({
family: "Arabic",
src: "/fonts/Cairo-Regular.ttf",
});
}

Call it once at module load — not per request.

2️⃣ Never render PDF in dev HMR path
if (process.env.NODE_ENV !== "production") {
return NextResponse.redirect(
new URL(`/invoices/${id}/preview`, request.url)
);
}

3️⃣ Do NOT cache PDF aggressively in dev

Your current headers:

"Cache-Control": "public, max-age=3600",

In dev, this causes:

browser cache + hard reload conflict

stale font state reuse

Use this instead:

"Cache-Control": "no-store",

🧪 Why HTML preview is the right solution
Feature HTML React-PDF
HMR ✅ ❌
Fast refresh ✅ ❌
Debuggable ✅ ❌
Fonts Easy Fragile
SVG Native Limited
RTL Excellent Bug-prone

All serious invoicing systems do this:

Stripe

Shopify

SAP

Oracle NetSuite

PDF is always export, never live view.

🧠 Final Answer to Your Question

“Is there a better way to use HMR and html instead of rendered PDF, or how can I design an invoice properly?”

✅ Yes — and you already reached the correct conclusion

Correct workflow:

Design invoice in HTML

Share a single view model

Generate PDF only:

on demand

in production

in isolated execution

Never rely on React-PDF during HMR

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
