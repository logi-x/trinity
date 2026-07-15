---
title: "Experts Home Partners Statsig"
date: "2026-06-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts Home Partners Statsig Config

Date: 2026-06-09
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Change

Moved the home page partners list and partner-specific localized display labels out of rendered source/i18n message keys and into Statsig dynamic config `home_partners`.

## Details

- Statsig dynamic config: `home_partners`
- Console name: `Home Partners`
- ID type: `stableID`
- Follow-up worktree: `/home/logix/experts-home-partners-skeleton` on branch `codex/home-partners-skeleton`
- Payload shape:

```json
{
  "partners": [
    {
      "name": "House of Wisdom Academy",
      "label": {
        "en": "House of Wisdom Academy",
        "ar": "أكاديمية بيت الحكمة",
        "es": "Academia de la Sabiduría"
      },
      "logo": "house-of-wisdom-academy.svg",
      "link": "https://www.howa.edu.sa"
    }
  ]
}
```

`logo` supports partner asset filenames, absolute paths, or full URLs. `label` is an optional locale map used for image alt text/display labels. The follow-up worktree removes `DEFAULT_PARTNERS`; while Statsig is loading, the component renders HeroUI skeleton placeholders instead of local partner data.

## Verification

- `npm run typecheck:touched -- 'app/(i18n)/_shared/(home)/(sections)/partners-section.tsx'`
- `./node_modules/.bin/eslint 'app/(i18n)/_shared/(home)/(sections)/partners-section.tsx' --no-warn-ignored`
- GitNexus `detect_changes`: low risk, one changed file.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
