---
title: "EXP-117: checkAndSendStorageAlerts hardcodes free-tier quota threshold"
linear_id: "EXP-117"
agent_fp: "ebf7ec8fc4cd"
spinoff_of: "EXP-113"
date: "2026-05-25"
severity: "Low"
status: "Backlog"
tags: [bug, storage, configuration, project/experts]
category: "bug"
source: "automation"
---

# EXP-117: checkAndSendStorageAlerts hardcodes free-tier quota threshold

**Linear:** EXP-117 | **Fingerprint:** `<!-- agent-fp: ebf7ec8fc4cd -->` | **Spinoff of:** EXP-113

## Summary

The `checkAndSendStorageAlerts` function (EXP-113 parent) hardcodes the free-tier storage quota threshold instead of reading it from the quota tier configuration table. When quota tier limits are updated, the alert thresholds drift silently.

## Impact

- Storage alert emails trigger at wrong thresholds after any quota tier change.
- Users receive "80% full" alerts at incorrect byte counts.
- Affects correctness of EXP-106's `StorageWarningNotification` emails.

## Root Cause

The function was implemented with a placeholder constant for the free-tier limit. The quota tier table (introduced with EXP-72) is the canonical source but was not wired into the alert function.

## Fix

Read the threshold from the quota tier record for the user's plan at runtime:

```ts
const tier = await db.storageTier.findFirst({ where: { plan: user.plan } });
const warningThreshold = tier.limitBytes * 0.8;
const limitThreshold = tier.limitBytes;
```

## Related

- EXP-113 (parent — dead checkAndSendStorageAlerts), EXP-106 (StorageWarningNotification emails)
- EXP-72 (quota gate, introduces tier table)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
