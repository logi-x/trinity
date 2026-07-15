---
title: "Experts Video Gate No Ended Shortcut"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts video completion gate no longer unlocks from seek-to-end

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Problem

Native gated video lessons could be bypassed by seeking to the end.

Two issues caused it:

- the client still allowed forward seeking anywhere in the timeline
- watch eligibility treated `ended = true` as equivalent to meeting the 95% coverage requirement

## Decision

Video completion eligibility is now based on actual watched coverage only.

- finishing the video after a forward seek does not unlock completion by itself
- forward seeking is clamped to the furthest contiguous watched position from the start of the video

## Implementation

- removed the `ended` eligibility shortcut from `video-watch-coverage.ts`
- added contiguous watched-end calculation to drive seek limits
- passed max allowed seek time from the lesson gate hook into the native video player
- clamped disallowed seeks in the player by snapping back to the last unlocked position

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
