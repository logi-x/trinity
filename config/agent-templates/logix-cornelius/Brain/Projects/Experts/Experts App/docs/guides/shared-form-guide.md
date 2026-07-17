---
title: "Shared Form Guide"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/shared-form-guide"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]

# Shared Form Guide

Q: I have two huge create/edit event forms, shouldn't they share the same exact logic, components, forms, with a very slight changes, instead of redundant duplicate logic, components, forms, ?

A: The rule you want to follow (this is the north star)

Create and Edit are the same form.
The difference is only: data source + submit behavior.

If you ever feel the need to fork logic, it’s usually a smell.

The mistake to avoid (what you’re feeling now)

❌ CreateEventPage.tsx
❌ EditEventPage.tsx
❌ Each with:

their own state

their own validation

their own components

90% identical logic

subtle bugs drifting over time

This always gets worse.

The correct mental model

Think in three layers, not pages.

1️⃣ Domain form (shared, pure, reusable)

This is the form itself, independent of create/edit.

events/
└─ form/
├─ EventForm.tsx 👈 single source of truth
├─ event.schema.ts 👈 zod / validation
├─ event.defaults.ts 👈 default values
├─ event.mapper.ts 👈 api ↔ form
└─ event.types.ts

This form:

Knows how to render

Knows how to validate

Does NOT know:

where data came from

where it’s submitted

2️⃣ Page-level orchestration (thin)
app/creator/events/
├─ new/page.tsx
└─ [id]/edit/page.tsx

Each page only handles:

Concern Create Edit
Load initial data ❌ ✅
Provide defaults ✅ ❌
Submit action create update
Redirect after create after update

Everything else is shared.

3️⃣ Side effects live outside the form

API calls

Toasts

Redirects

Mutations

Never inside the form.

Concrete example (simplified)
Shared form component
// events/form/EventForm.tsx
export function EventForm({
initialValues,
onSubmit,
submitLabel,
}: {
initialValues: EventFormValues;
onSubmit: (values: EventFormValues) => Promise<void>;
submitLabel: string;
}) {
const form = useForm({
defaultValues: initialValues,
resolver: zodResolver(eventSchema),
});

return (

<form onSubmit={form.handleSubmit(onSubmit)}>
<EventFields form={form} />
<Button type="submit">{submitLabel}</Button>
</form>
);
}

Create page
export default function CreateEventPage() {
return (
<EventForm
      initialValues={eventDefaults}
      submitLabel="Create Event"
      onSubmit={createEvent}
    />
);
}

Edit page
export default function EditEventPage({ params }) {
const event = useEvent(params.id);

if (!event) return <Loader />;

return (
<EventForm
initialValues={mapEventToForm(event)}
submitLabel="Save Changes"
onSubmit={(values) => updateEvent(params.id, values)}
/>
);
}

What changes between create & edit (allowed differences)

These are valid differences:

Submit button text

API endpoint

Redirect destination

Initial values source

Disabled fields (e.g. slug)

These are NOT valid differences:

Field components

Validation rules

Layout

State management

Form logic

How this fixes your 1600-line TSX problem

Instead of:

CreateEventPage.tsx (1600 lines)
EditEventPage.tsx (1500 lines)

You get:

EventForm.tsx (600–800 lines max)
Create page (50 lines)
Edit page (80 lines)

And now:

You change a field once

Validation is consistent

UX stays aligned

Bugs don’t drift

When NOT to share (important)

Don’t force sharing if:

Create and Edit are conceptually different workflows

e.g. “Quick Create Wizard” vs “Advanced Edit”

Different audiences

Different permissions

That’s not your case here.

Rule of thumb (save this)

If two forms share more than 60% of fields and logic → they are one form.

You’re at ~90%.

Final answer (direct)

✅ Yes, they should share:

the same form

the same fields

the same validation

the same components

❌ They should NOT duplicate logic

Q: What about a specific gated logic, like for example limited event creating count, and free plan users can't create paid events, etc...

A: Great question — this is exactly where people either pollute the form with business rules or design it cleanly once and never regret it again.

Short answer first, then the correct structure.

Short answer (important)

Gating logic is NOT form logic.
It is orchestration + policy logic.

So:

❌ Do NOT bake plan limits, permissions, or business rules into the form

✅ The form should stay dumb and reusable

✅ Gating happens before render and before submit

The correct mental model

There are three distinct layers, and they must stay separated:

Policy (can user do X?)
↓
Orchestration (create vs edit flow)
↓
Form (pure UI + validation)

Where each rule belongs (very concrete)
1️⃣ Plan / entitlement checks

→ Page-level or route-level

Examples:

Free plan: max 1 event

Free plan: cannot create paid events

Pro plan: unlimited

These checks decide:

Can the page render?

Should some fields be disabled?

Should we show an upsell?

❌ NOT inside the form
❌ NOT inside field components

✅ Before the form even renders

2️⃣ Feature gating (field-level)

→ Orchestration layer (props to form)

Example:

“Paid event” toggle disabled for free plan

Price input locked

Tooltip: “Upgrade to enable paid events”

The form receives capabilities, not rules.

<EventForm
capabilities={{
    canCreatePaidEvent: false,
    maxTickets: 50,
  }}
/>

Form logic becomes:

{capabilities.canCreatePaidEvent && <PriceField />}

The form doesn’t know why — and shouldn’t.

3️⃣ Enforcement (security)

→ Backend, always

Even if UI hides it:

API must reject paid events for free users

API must enforce limits

API must be the final authority

Frontend gating = UX
Backend gating = truth

Example: limited event creation count
Page-level logic
const entitlements = useEntitlements();

if (!entitlements.canCreateEvent) {
return <UpgradeNotice />;
}

Form never renders.

Example: free plan can’t create paid events
Page orchestration
<EventForm
initialValues={...}
capabilities={{
    canCreatePaidEvent: entitlements.plan !== "free",
  }}
/>

Inside the form
<Switch
  label="Paid Event"
  disabled={!capabilities.canCreatePaidEvent}
/>

Optional UX:

Tooltip

Upgrade CTA

Inline hint

Example: edit mode exception

Free user can edit a paid event created earlier (edge case)

That logic belongs outside the form:

const canEditPrice =
entitlements.plan !== "free" || event.isPaid === true;

Then:

<EventForm capabilities={{ canEditPrice }} />

Again:

Form doesn’t know why

Only knows what is allowed

Why this scales cleanly

When you later add:

team plans

event quotas

enterprise overrides

admin impersonation

You update:

entitlement resolver

orchestration layer

You do not touch:

form fields

validation

layout

components

This is exactly what you want.

Common anti-patterns (avoid these)

❌ if (user.plan === "free") inside form
❌ API calls inside form fields
❌ Validation rules changing per plan
❌ “Smart” form components with business logic

These always explode later.

Rule of thumb (save this)

Forms render possibilities.
Pages decide permissions.
Backend enforces truth.
