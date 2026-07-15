---
title: GitHub Flow
date: 2026-05-18
source: "generated"
source_id: "Raw/conversations/github-flow.md"
tags: [github, flow, project/experts, app]
category: "conversation"
---

Q: I'm in a sort of predicament, as I think my github's workflow is sort of off, the I do things now

let's say I found a security issue, fixed it -> commit -> push -> open a PR to main

in that PR comment there's something like

```md
## Test plan

- [x] Targeted vitest — 16/16 new + 8/8 upload regression pass
- [x] tsc + eslint — green
- [ ] Manual smoke (post-Traefik handoff): trigger a CSP violation in browser dev tools → observe `csp.violation` warn event in observability pipeline with normalized fields
- [ ] Manual smoke: send 61 rapid POSTs from one IP → confirm the 61st gets silent-drop and no `csp.violation` event is emitted server-side
```

but it's not possible to test it until I close the PR -> manually run the stg/prd release workflow so changes can get to the stg/prd servers then I can test if it actually worked or not!!!

A: Yes — your workflow is slightly off.

The missing piece is:

```txt
PR branch should be deployable to staging before merge.
```

Not:

```txt
merge PR → deploy staging → test → hope it worked
```

Better flow:

```txt
security-fix branch
→ open PR to main
→ CI runs automated checks
→ deploy this PR/branch to staging
→ run manual smoke tests
→ update PR checklist
→ merge to main
→ deploy production
```

So your PR test plan becomes truthful.

Your staging release workflow should support an input like:

```yaml
branch:
  description: "Branch/ref to deploy to staging"
  required: true
  default: "main"
```

Then you can manually deploy:

```txt
security/csp-rate-limit-fix → staging
```

test it, then merge.

For production, keep it stricter:

```txt
production deploys only from main/tags
```

So the recommended model is:

```txt
Any branch/PR → staging
main/tag only → production
```

Your checklist then becomes:

```md
## Test plan

- [x] Targeted vitest — 16/16 new + 8/8 upload regression pass
- [x] tsc + eslint — green
- [x] Staging deployed from this PR branch
- [x] Manual smoke: trigger CSP violation → observed `csp.violation`
- [x] Manual smoke: send 61 rapid POSTs → 61st silently dropped
```

This solves the contradiction.

You don’t need to close/merge the PR before testing. You need your **staging deployment workflow to accept a branch/ref**, while production stays protected.
