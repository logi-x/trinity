---
title: 'Experts App Changelog'
latest_version: '1.1.9'
current_unreleased_version: '1.2.0'
latest_version_date: '01-06-2026'
latest_version_status: 'released'
latest_version_started: '08-05-2026'
latest_version_released: '01-06-2026'
latest_released_tag: v1.1.9-stable
latest_released_date: '01-06-2026'
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
---

> ↑ [[Entities/Projects/Experts App|Experts App]]

# Changelog

This page lists **what changed** in Experts platform, grouped by release and date.

> [!IMPORTANT]
> Release channels — alpha → beta → RC → stable
>
> We ship **numbered snapshots** along one version line (for example **1.1.8**) instead of a single undecorated tag like `v1.1.8`. Tags combine the version, a **channel**, and usually a **build number**, for example **`v1.1.8-alpha.1`**, **`v1.1.8-beta.2`**, **`v1.1.8-rc.1`**, **`v1.1.8-stable`**. Each channel is a checkpoint against **specific readiness criteria**.
>
> **Progression:** **alpha** → **beta** → **RC** (release candidate) → **stable**.
>
> #### Alpha
>
> - **Expect:** Very unstable; **internal-only**, **experimental** work.
> - **Example:** `v1.1.8-alpha.1` — first experimental build of the 1.1.8 line.
>
> #### Beta
>
> - **Expect:** **Feature-complete-ish**; **testing** phase; **bugs still expected**.
> - **Example:** `v1.1.8-beta.3` — third beta build on the way to release.
>
> #### RC (release candidate)
>
> - **Expect:** **Almost production-ready**; if **no major issues** show up in validation, this line is promoted to **stable**.
> - **Example:** `v1.1.8-rc.1`.
>
> #### Stable
>
> - **Expect:** **Production-ready**; **official** release customers should run in production for that line.
> - **Example:** `v1.1.8-stable`.

---

> [!NOTE]
>
> **Version 1.1.9** covers work through **08 May 2026** to **01 June 2026**;
>
> **Version 1.1.8** covers work through **04 May 2026** to **08 May 2026**;
>
> **Version 1.1.7** covers work through **17 April 2026** to **04 May 2026**;
>
> **Version 1.1.6** covers work through **14 April 2026** to **17 April 2026**;
>
> **Version 1.1.5** covers work through **04 April 2026** to **14 April 2026**;
>
> **Version 1.1.4** covers work through **26 March 2026** to **04 April 2026**;

---

<details>
<summary><strong>[1.1.9] — 08-05-2026 - 01-06-2026</strong> — re-written to a readable format</summary>

<br />

[Google Docs V1.1.9](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit)

> [!NOTE]
>
> **Metadata for this version:**
>
> ```markdown
> version: "1.1.9"
> date: "01-06-2026 "
> status: "released"
> started: "2026-05-08"
> released: "01-06-2026"
> latest_channel_tag: "v1.1.9-rc.9"
> latest_production_release: "v1.1.8-stable"
> commit_range: "44eff14287f3406394206e8a0359eec7008b622e..45fceafc48bd0df7573f9c4b85627825777aa9d5"
> tags:
> - "v1.1.9-alpha.1"
> - "v1.1.9-beta.1"
> - "v1.1.9-beta.2"
> - "v1.1.9-beta.3"
> - "v1.1.9-beta.4"
> - "v1.1.9-beta.5"
> - "v1.1.9-beta.6"
> - "v1.1.9-rc.4"
> - "v1.1.9-rc.5"
> - "v1.1.9-rc.6"
> - "v1.1.9-rc.7"
> - "v1.1.9-rc.8"
> - "v1.1.9-rc.9"
> - "v1.1.9-stable"
> ```

### 2026-05-31

> [!NOTE]
> **1.1.9** — 08-05-2026 - 01-06-2026. Summary synthesized from **409 commits** after **`44eff142`** through **`45fceafc`**.

### What to test since last release?

**1.1.9** includes all changes since **1.1.8** (started **08 May 2026**). Focus areas for learners, creators, admins, and platform ops:

#### Security, CSP, and upload hardening

- **Incident remediation (#1–#15):** broad hardening across **internal upload**, **thumbnail ownership**, **per-user upload rate limits**, **pending→ready** object lifecycle, **storage janitor**, **buffer size rechecks**, **defense-in-depth headers**, **course detail / presence / viewers** anonymous exposure fixes, **CSP nonce + Report-Only → enforcing CSP** (Phases 4A/4B), **CSP violation reporting**, **MIME→extension** derivation for R2 keys (not filenames), **inline-renderable MIME allowlist**, **RFC 5987** filenames, and **cookie-scope** regression tests.
- **HTTP boundary & paywall (EXP-68 family):** paid course content gating completed; enrolled learners retain access when a course is temporarily unpublished.
- **Error disclosure sweep (EXP-170 family):** **`safeErrorJson`**, **`DomainError`**, ESLint sink rule for **`src/lib`**, and route-level tests — no raw **`error.message`** / stack in API responses.
- **Cron auth:** **timing-safe `CRON_SECRET`**, fail-closed when unset, removal of **length-oracle** comparisons.
- **Realtime security (EXP-174):** sync route **IDOR** fixes, **channel caps**, **ReDoS** guards; removed unauthenticated **share/test** diagnostic endpoint.

#### Storage, R2, quotas, and course-scoped uploads

- **Unified asset model:** **`lesson_resources` dropped**; **`course_lesson_assets`** / flat **`CourseAsset`** XOR (**`attachmentId` / `url`**) with schema **`course_*` naming** standardization and quiz option renames.
- **Upload tree:** **course-scoped paths** (`uploads/courses/<id>/…`); **pending-first** uploads for community thumbnails, lesson video, and related domains; **PUT-first guardrail**; **R2 orphan reaper decommissioned** (EXP-231) in favor of janitor sweeps.
- **Quota ledger:** race-safe **reservations**, **`File.size` → BigInt**, **decrement on delete**, tier-aware **storage alerts** (EXP-117/118/121/126), **admin storage dashboard**, **`checkAndSendStorageAlerts`** wired to Docker cron.
- **Storage janitor:** **orphan-attachment sweep**, **pending-file sweep** (bounded), **bucket-aware deletes**, env-isolation gates, cron entries in **staging/production** compose (6h orphan sweep, 15m reservation cleanup, etc.).
- **CDN & health:** mappers emit **direct CDN URLs** where appropriate; health check flags **missing R2 upload buckets**.

#### Ask AI, embeddings ops, and conversation lifecycle

- **`AskAiConversation.deletedAt`:** soft-delete migration shipped; **in-transaction re-check** before persisting exchanges (EXP-239).
- **Conversation UX & safety:** **abort in-flight stream** before loading another conversation (EXP-222); **200-message cap**, newest-first fetch (EXP-205); **rate limits** on conversation management routes (EXP-206); **UUID guards** + try/catch on **`[id]`** routes (EXP-221); **sanitized SSE error codes** (EXP-207).
- **Route visibility:** **deny-list replaced** with explicit allow model for Ask AI surfaces.
- **Build/runtime:** lazy **OpenAI client** so **`next build`** does not require **`OPENAI_SECRET`** (EXP-181).

#### Courses, curriculum, recognition, and instructor workflows

- **Course recognition type (Phases 08–09):** Prisma columns **`recognitionType`** + **`recognitionReviewStatus`**, Zod enums, **eligibility on create/update/publish**, **recognition-review scanner** with revoke/approve side effects, admin UI and domain tests.
- **Lifecycle & roles:** **DB-fresh / DB-authoritative role checks** across course create, modules, lessons, and quizzes (EXP-197/199/212/213); **`approvalStatus: pending`** on submit (EXP-214); **archive / delete dialogs** on course overview; archived course rendering fixes.
- **Lesson assets API:** rebuilt CRUD after resource drop; **attachment ownership** verification before link (EXP-50); quiz-question image upload domain fix (incident #15).
- **Progress & validation:** UUID validation before Prisma on progress routes (EXP-79); title must **start with a letter** for courses/events (EXP-95).

#### Payments, checkout, and Tabby (EXP-96 / EXP-99+)

- **Tabby (BNPL):** **KSA-only** eligibility, checkout UI shows **disabled/unavailable** states with **billing-address** guidance when ineligible; CSP **`connect-src` / frame** allowances for Tabby domains.
- **Provider hardening:** sanitized **Noon** name fields with gateway tests (EXP-94); **fail-closed `CF_ORIGIN_SECRET`** on non-production (EXP-123); checkout failures no longer leak raw provider payloads (EXP-201).

#### Realtime, community, and social

- **Sync polling:** **rate limits** (EXP-191); **bounded queries** in sync sections 2–3 (EXP-192/194); **strict channel isolation** for post likes (EXP-193); **strip `userId`** from public like events for non-actors (EXP-195).
- **Community validation:** shared **Zod schema** for post create + update (EXP-224/240).
- **WebSocket UX:** debounced leader kicks and deduped connects.

#### Auth, SEO, and session stability

- **`src/lib/auth/` package:** consolidated auth modules (EXP-200).
- **Canonical origin:** centralized app URL — stops **staging URLs leaking** into production metadata/links (EXP-204/216/217/218); removed redundant **`NEXT_PUBLIC_SITE_URL` / `NEXT_SITE_URL`** (EXP-219).
- **Login regression fix:** stop **whole-app remount** on auth session changes (EXP-225).
- **Proxy:** **`/creator` route guard** restored (EXP-53).

#### Certifications, certificates, and company collateral

- **Phase 07:** deep **certification schema / domain migration** and UI cutover hygiene.
- **Certificates:** **`courseTitle` always from DB**, not POST body (EXP-75); certification **resubmit validation** and **`normalizedFieldId`** on approve.
- **Company showcase:** invoice / letterhead / business-card **print and watermark** improvements; collateral sections reordered; deprecated English-only showcase removed.

#### Ops, Docker, CI/CD, and database guardrails

- **Docker cron sidecar:** **`APP_BASE_URL`** restored for scheduled jobs (EXP-175); **`CRON_SECRET`** hidden from process args (EXP-152); Redis/Postgres **loopback-only** bindings; pinned Redis images; **Node 24-alpine** app images.
- **Prisma in containers:** **`DATABASE_URL`** hydrated from Docker secrets in migrate job (EXP-190).
- **CI:** **migration-drift guard** (EXP-227); production deploy **gated on main/tags**; **Slack #experts-deployments** notifications; **`force_build_app`** workflow input; **`APP_VERSION`** on deploy jobs.
- **Secrets & env:** `.env` / secrets removed from git history patterns; quoted **print watermark** env values; tightened **runtime/build secret** flow (EXP-168).

#### Agents, routines, and engineering tooling

- **Cursor / Claude routines:** pool dispatcher, worktree setup, **R7/R8/R9** audits (codebase completeness, Linear board, routines security), **pre-flight clean git slots**, verbose local runner, **EXP-158/161/162** collateral filing markers.
- **Subagents:** accessibility, AI engineer, analytics architect, architecture/code reviewer, concept architect, DB engineer, **codebase-completeness** and **linear-board** auditors.
- **GitNexus:** index refresh, skill description normalization, changelog structure updates.

#### UI polish and learner/creator surfaces

- **Global alert-dialog sweep** and course **archive/delete** confirmations.
- **Course detail:** enrollment handling and **`useApiQuery`** structure improvements.
- **Creator event detail:** role staleness fix.
- **Admin:** embeddings UI moved under **admin AI** section.

### Raw entries (by date)

### 2026-05-04

> [!NOTE]
> Pre-release build — behaviour should match production, but we still recommend a quick pass on the areas below before you rely on it for a big launch.

Update environment files to quote watermark text

- Modified the NEXT_PUBLIC_PRINT_WATERMARK_TEXT variable in production, staging, and prsma environment files to ensure proper quoting of the watermark text.
- Added a comment in entrypoint.sh to clarify the need for quoting values with spaces or metacharacters when sourcing environment files.

Update experts-app.yml to set APP_VERSION for deployment jobs

- Added APP_VERSION environment variable to deployment jobs, defaulting to 'undefined' if not set, to enhance clarity in deployment configurations.

Update docker-compose files for production and staging environments (#302)

- Set APP_VERSION to 'undefined' in both production and staging
  configurations for clarity.
- Refactor healthcheck and command syntax for PostgreSQL and Redis
  services to improve readability and maintainability by using array
  format.
- Commented out the experts-stg-deploy service in the staging
  configuration for future reference.
  Update docker-compose files for production and staging environments

- Set APP_VERSION to 'undefined' in both production and staging configurations for clarity.
- Refactor healthcheck and command syntax for PostgreSQL and Redis services to improve readability and maintainability by using array format.
- Commented out the experts-stg-deploy service in the staging configuration for future reference.

Bug/course creation flow (#301)
Feat/add ai worker (#300)
Enhance/company profile showcase (#299)
Update showcase sections for invoice and letterhead components

- Reordered the section labels in the InvoiceSection and LetterheadSection to maintain consistent numbering.
- Reintroduced the LetterheadSection in the ExpertsShowcaseV2Page for improved visibility in the company profile showcase.
- Enhanced the layout and organization of the showcase components for better user experience.

Refactor invoice showcase to support multiple variants

- Replaced the single invoice preview with a new structure that supports multiple invoice variants, enhancing flexibility for branding and localization.
- Introduced `InvoiceVariant` type to manage different invoice configurations.
- Updated the `InvoiceSection` to display variants and improved the layout for better user experience.
- Added `InvoiceDisplayCards` component for dynamic variant selection and display.
- Adjusted invoice rendering logic to accommodate bilingual support and branding customization.

Remove unnecessary whitespace from Letterhead.tsx file to improve code cleanliness.

Remove English company profile showcase page implementation

- Deleted the English version of the company profile showcase page to streamline the codebase.
- This change eliminates outdated logic and prepares for future updates to the company profile features.

Update business card and letterhead components for improved print functionality

- Added new print-specific CSS modules for business cards and letterheads to enhance print layout and visibility.
- Introduced a new JSON file for auto-memory storage related to task outcomes.
- Refactored existing components to streamline print processes and improve maintainability.
- Removed outdated business card styles and PDF files to reduce clutter and ensure consistency in design.
- Enhanced the overall structure and organization of business card components for better responsiveness and visual appeal.

Enhance company profile print features and layout

- Introduced new components for printing the company profile, including sections for About, Catalog, Contact, and Experts.
- Implemented a toolbar for print functionality and added a watermark feature for print documents.
- Updated styles and layout for improved visual consistency across print sections, ensuring bilingual support for Arabic and English.
- Refactored existing components to streamline the print process and enhance maintainability.
- Added new CSS for print-specific styles, including a paper-grain texture for visual depth.

Add letterhead document and update styles

- Introduced a new binary file for the letterhead document.
- Removed the outdated letterhead.module.css file and replaced its styles with Tailwind CSS classes in Letterhead.tsx and LetterheadGenerator.tsx.
- Updated the layout and styles for the letterhead components to enhance visual consistency and maintainability.
- Refactored print and screen layouts to improve rendering fidelity and responsiveness.

Remove invoice preview components and related documentation

- Deleted the invoice preview page and associated markdown documentation to streamline the codebase.
- This change eliminates outdated logic and prepares for a unified invoice rendering approach using the new InvoiceViewModel.

Enhance company profile showcase and invoice features

- Updated the company profile page to redirect the secondary call-to-action button to the showcase section.
- Added a new icon to the button for improved visual appeal.
- Refactored the showcase page layout, introducing new styles and class constants for better organization and readability.
- Removed the outdated showcase.module.css file to streamline the codebase.
- Updated translations for the secondary call-to-action in multiple languages to reflect the new showcase terminology.
- Enhanced invoice rendering components to include copyright information in both HTML and PDF formats, ensuring compliance and branding consistency.

Add typography section and new font styles

- Introduced a new `fonts.css` file to define custom font faces for "Sultan" and "Proxima Nova", along with "Muna" for Arabic typography.
- Updated `globals.css` to import the new font styles and added variables for "Changa" and "Ubuntu Mono".
- Enhanced the company profile showcase page with a dedicated typography section, showcasing bilingual type systems for English and Arabic.
- Implemented new styles in `showcase.module.css` to support the typography layout and improve visual presentation.
- Added metadata generation for company profile and invoice pages to enhance SEO and structured data support.

Implement invoice showcase and preview features

- Added invoice showcase section to the company profile, including a sample tax invoice preview.
- Introduced new components for rendering invoices in HTML and PDF formats, ensuring consistent presentation.
- Enhanced styles for invoice display, aligning with existing collateral designs.
- Created new routes for invoice loading and previewing, improving user access to invoice data.
- Updated letterhead and business card components to support watermark features in both screen and print views.

Update GitNexus indexing and enhance business card watermark features

- Updated GitNexus indexing information to reflect increased symbols and relationships.
- Added environment variables for print and business card watermarks in production, staging, and Prisma environment files.
- Implemented watermark display logic in business card components, ensuring visibility in previews while omitting in print.
- Enhanced showcase pages with updated styles and layout adjustments for better presentation of business cards and collateral.

Add AI generate worker foundation

Update package.json scripts for type checking and formatting

- Renamed "prepare" and "prepare:fix" scripts to "check" and "check:fix" for clarity.
- Maintained concurrent execution of formatting, linting, and type checking tasks.

Preserve pure AI worker queue contract

Move admin embeddings UI under admin AI

Remove deprecated .env.canary file and update environment configurations for AI worker and embedding sync

- Deleted the obsolete .env.canary file to streamline environment management.
- Added AI worker concurrency and limiter settings to various environment files (.env.e2e, .env.example, .env.production, .env.prsma, .env.staging) for improved AI processing control.
- Updated embedding sync routes and handlers to ensure proper integration with the new AI embedding service, enhancing the overall functionality of the application.

Enhance AI embedding and observability features

- Introduced a new embedding service to handle real-time embedding for courses, events, and posts, improving the efficiency of AI processing.
- Implemented observability tracking for embedding jobs, including success and error states, to enhance monitoring and debugging capabilities.
- Updated various publish handlers to enqueue embedding jobs upon creation, ensuring immediate processing without blocking responses.
- Added a dedicated processor for handling embedding jobs, separating concerns and improving code organization.

Add AI debug configuration and observability enhancements

- Introduced DEBUG_AI environment variable in production and staging configurations to control AI-related debugging.
- Updated observability logic to include AI event tracking, allowing for better monitoring of AI-related activities.
- Modified the reportToZatca function to streamline debug observation for ZATCA responses.

Make worker release script executable

Add worker image release flow

Add AI worker service configuration to Docker Compose

- Introduced a new service for the AI worker in the production Docker Compose file, enabling pure compute capabilities for embeddings and job processing.
- Configured environment variables for Redis and database connections, along with AI worker concurrency and limiter settings.
- Set up logging, command execution, and volume mounts for the AI worker service, ensuring proper integration with existing services.

Add production AI worker service

Add AI worker functionality and integrate AI job handling

- Introduced a new AI worker for processing jobs related to AI capabilities, ensuring a pure compute environment without database access.
- Added AI job queue management using BullMQ, allowing for efficient job handling and result processing.
- Implemented AI result handling to manage job completion and errors, enhancing observability and error tracking.
- Updated package.json to include new worker scripts for AI processing and modified the all command to incorporate the AI worker.
- Configured Docker to support the new AI worker, ensuring proper environment variable management and service dependencies.

Update GitNexus indexing and enhance experts-app configuration

- Updated GitNexus indexing details in AGENTS.md and CLAUDE.md to reflect new symbol and relationship counts.
- Improved formatting in resource and CLI sections for better readability.
- Modified Dockerfile.worker to include pnpm workspace configuration and updated dependency management.
- Renamed package.worker.json to reflect a more accurate package name and description, and added TypeScript and tsup as devDependencies.
- Introduced pnpm-workspace.worker.yaml for build configuration.
- Enabled minification in tsup configuration and added openai as an external dependency.

Add moduleAssets property to curriculum test data

- Updated the `makeModules` function in the module-dnd-utils test file to include a `moduleAssets` property in the generated module data, ensuring comprehensive test coverage for module asset management.

Add module assets management to curriculum

- Introduced `ModuleAssetsTab` component to display assets associated with selected modules in the learning page.
- Updated `Module` type to include `moduleAssets` for better data handling.
- Enhanced curriculum management by adding functions to add and remove module assets in the curriculum logic.
- Created `ModuleAssetsPanel` for managing module assets, allowing uploads and links to be added.
- Implemented API routes for creating and deleting module assets, ensuring proper authorization and validation.
- Added internationalization support for module asset messages in Arabic, English, and Spanish.

Enhance AI Suggest functionality and curriculum management

- Updated AI Suggest context to include course and module details, improving suggestion accuracy.
- Modified curriculum components to accept course title and description, enhancing user experience.
- Refactored curriculum dialogs to utilize AI Suggest for generating titles and summaries, streamlining content creation.
- Adjusted API input schema to accommodate new context fields for better integration with AI suggestions.
- Improved curriculum report generation to reflect updated node and edge counts, enhancing data insights.

Enhance curriculum upload functionality and internationalization support

- Updated `ensureLessonForUpload` function to accept an additional `uploadKind` parameter, allowing differentiation between video and asset uploads.
- Modified error messages in the lesson upload process to reflect the type of upload being performed.
- Updated relevant components to utilize the new `uploadKind` parameter for asset uploads.
- Added new internationalization strings for asset upload error messages in Arabic, English, and Spanish.

Refactor AI Suggest components and course form handling

- Replaced Popover with Modal in AiSuggestButton and AiSuggestListButton for improved user experience.
- Updated state management in AiSuggestListButton to use deselection logic.
- Enhanced course form payload mappers to normalize learning outcomes, requirements, and tags.
- Added unit tests for course form payload mappers to ensure correct normalization behavior.

Enhance experts-app configuration and UI components

- Added new `prepare` and `prepare:fix` scripts to streamline development tasks in the experts-app.
- Updated the `CreatorEnrollmentsPage` to utilize a loading state with improved user feedback.
- Refactored `CreatorSidebarShell` to replace the loader with a new `CreatorContentLoader` component for better loading indication.
- Enhanced `EventCard` layout for improved spacing and added event date and registration details.
- Introduced a new utility function for upcoming event queries in the recommendations module.
- Updated Docker commands for local development to reflect new container names and configurations.

</details>

---

<details>
<summary><strong>[1.1.8] — 04-05-2026 - 08-05-2026</strong> — re-written to a readable format</summary>

<br />

[Google Docs V1.1.8](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?tab=t.xm6vboeaftpj)

### 2026-05-04

### -

> [!WARNING]
> SKIPPED IN FAVOR OF 1.1.9

</details>

---

<details>
<summary><strong>[1.1.7] — 18-04-2026 - current</strong> — expand for full notes</summary>

<br />

[Google Docs V1.1.7](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?tab=t.nb3j8xqi8mgh)

### 27-04-2026 - 04-05-2026

> [!NOTE]
> RELEASE CANDIDATE

#### Features: embeddings recommendations, AI knowledge sync, and Ask AI assistant, and company profile (#268)

- docs(phase-15): research embeddings and recommendations foundation

- docs(15): create phase 15 embeddings foundation plan (5 plans, 4 waves)

- docs(phase-15): plan embeddings & recommendations foundation

Adds Phase 15 to ROADMAP + REQUIREMENTS (EMBED-01–05), creates full
planning artifacts: RESEARCH, PATTERNS, VALIDATION, and 5 PLAN.md files
across 4 waves covering pgvector schema, sync service/worker, cron
endpoint, publish hooks, and admin debug page.

- chore(15-01): swap Docker Postgres images to pgvector/pgvector:pg16

- docker/data/docker-compose.yml: postgres:latest -> pgvector/pgvector:pg16
- docker/staging/docker-compose.yml: postgres:latest -> pgvector/pgvector:pg16

- feat(15-01): add ContentEmbedding and EmbeddingSync Prisma models + vector migration

- Append ContentEmbedding model (vector(1536) embedding column, unique on entityType+entityId+locale)
- Append EmbeddingSync model (status queue, unique on entityType+entityId)
- Both models follow project conventions: @Map snake_case, @db.Timestamptz(6), @@Schema("public")
- Manual migration SQL: CREATE EXTENSION IF NOT EXISTS vector before CREATE TABLE DDL
- pnpm prisma validate and pnpm db:generate pass; migrate dev deferred pending Docker restart

- docs(15-01): execution summary

- feat(15-02): add recommendations domain DTOs, command types, and status query

- EmbeddingSyncEnqueueCommand with EntityType union type
- EmbeddingSyncStatusDTO, EmbeddingSyncRow, EmbeddingSyncStatusResponse interfaces
- getEmbeddingSyncStatus() parallel count query returning pending/synced/failed + last 20 rows

- feat(embedding-sync): implement embedding sync service and worker

- Add embedding-sync.service.ts to handle fetching entity text and processing embedding rows.
- Introduce embedding-sync.worker.ts to manage batch processing of embedding sync tasks, ensuring compliance with OpenAI rate limits.
- Utilize Prisma for database interactions and observability for monitoring sync operations.

- chore: update project state to Phase 15 In Progress

- Changed status to reflect Phase 15 execution start
- Updated stopped_at message to indicate current phase activity
- Increased total plans from 24 to 29
- Updated last_updated timestamp to the current date

- docs(phase-15): record recommendations domain plan completion

- feat(15-03): Add embeddings sync cron route

- Add internal embeddings sync POST route with cron secret auth
- Schedule the Vercel cron worker every two minutes

- docs(phase-15): record embedding cron plan completion

- feat(15-04): enqueue embeddings for course and event publish

- add fire-and-forget course EmbeddingSync upsert on publish
- add fire-and-forget event EmbeddingSync upsert for published creation

- feat(15-04): enqueue embeddings for community posts

- docs(phase-15): record publish hook plan completion

- feat(15-05): add embeddings admin debug page

- docs(phase-15): record embeddings admin plan completion

- fix(15-02): keep failed embedding rows for admin retry

- docs(phase-15): add code review report

- test(15): persist embedding verification UAT

- feat(gitnexus): add new skills for GitNexus CLI, debugging, exploring, impact analysis, refactoring, and guide

- Introduced `gitnexus-cli` for command execution.
- Added `gitnexus-debugging` for tracing errors and debugging.
- Created `gitnexus-exploring` for understanding code architecture.
- Implemented `gitnexus-impact-analysis` for assessing code changes.
- Developed `gitnexus-refactoring` for safe code restructuring.
- Added `gitnexus-guide` for referencing tools and workflows.

- chore(cron): move scheduled jobs to docker sidecar

- feat(statsig): integrate Statsig for user analytics and session replay

- Updated dependencies for Statsig integration.
- Added MyStatsig component to manage user state and session synchronization.
- Wrapped application providers with MyStatsig for enhanced analytics capabilities.

- feat(statsig): enhance user onboarding and analytics integration

- Added Statsig context API to fetch user-specific analytics data.
- Implemented onboarding page for creators with step-by-step guidance.
- Integrated global banner for promotional messages and user engagement.
- Updated settings to include new Statsig server configurations.
- Refactored components to utilize Statsig for user state management and session tracking.

- feat(course-detail-tabs): enhance tab animations and accessibility

- Introduced motion animations for tab transitions using framer-motion.
- Updated tab components to include accessibility attributes such as aria-labels.
- Refactored tab layout for improved responsiveness and user experience.

- feat(recommendations): add unified related content cards

- chore(dependencies): update package versions and add environment variable

- Updated various dependencies in package.json and pnpm-lock.yaml for improved stability and features.
- Added NEXT_PUBLIC_STATSIG_CLIENT_KEY to .env.staging for Statsig integration.

- fix(recommendations): show fallback related content

- refactor(api): rename OPENAI_API_KEY to OPENAI_SECRET across the application

- Updated environment variable references from OPENAI_API_KEY to OPENAI_SECRET in .env.example, service files, and documentation.
- Adjusted related comments and documentation to reflect the new naming convention for clarity and consistency.

- chore(dependencies): update AWS SDK and related packages in pnpm-lock.yaml

- Upgraded AWS SDK packages to versions 3.1038.0, 3.974.6, and other related dependencies for improved functionality and security.
- Updated various other dependencies to their latest versions to ensure compatibility and stability.

- fix(docker): update staging data backup filenames and Redis password handling

- Changed the staging data backup filename from staging_data_backup_18-04-2026.sql to staging_data_backup_28-04-2026.sql in commands.md.
- Updated docker-compose.yml to reflect the new backup filename and made Redis password handling more flexible by using an environment variable.

- feat(recommendations): add user-driven dashboard recommendations

- feat(marketing): highlight AI platform features

- feat(features-page): enhance button styles and update card borders

- Updated button styles using utility functions for consistency.
- Changed card border radius from rounded-2xl to rounded-3xl for a more modern look.
- Removed unnecessary background classes to streamline the layout.

- feat(features-page): expand discovery features and improve layout

- Added 'semantic' filtering option to DISCOVERY_ITEM_KEYS for enhanced search capabilities.
- Updated section IDs for better accessibility and navigation.
- Improved layout of AI features section for better visual consistency and user experience.
- Enhanced internationalization support with detailed descriptions for new filtering options in English, Arabic, and Spanish.

- Codex/ask ai global assistant (#267)

- feat(ai): add admin ask ai assistant

- feat(ai): enhance Ask AI assistant with new features and improvements

- Added typing indicator for better user experience during message processing.
- Implemented message copy functionality and conversation clearing options.
- Updated internationalization strings to reflect the assistant's beta status.
- Refactored textarea component to support forwarding refs for better integration.
- Improved message handling and scrolling behavior in the assistant interface.

- feat(ai): enhance Ask AI assistant with conversation management and user permissions

- Introduced new modes (learner, creator, admin) for the Ask AI assistant to tailor responses based on user roles.
- Implemented conversation ID handling to track user interactions.
- Updated rate limiting logic to differentiate between user modes.
- Enhanced error handling for conversation-related issues.
- Added database models for storing Ask AI conversations and messages.
- Improved internationalization support for new features and modes.

- feat(ai): implement AI knowledge sync and retrieval features

- Added a new API route for syncing curated AI knowledge documents, including error handling for OpenAI API responses.
- Introduced database models for AI knowledge documents and chunks, enabling structured storage and retrieval.
- Implemented chunking and embedding of knowledge text for efficient processing and retrieval.
- Enhanced the Ask AI assistant with curated legal context for refund and policy questions, improving response accuracy.
- Added tests for the new sync route and retrieval logic to ensure functionality and reliability.

- fix-features-page and update-locales

- feat(features-page): update search functionality and improve layout

- Added new search feature with placeholder and results in English, Arabic, and Spanish.
- Enhanced layout of the features page for better visual consistency.
- Removed unused AI future keys and icons for cleaner code.
- Improved internationalization support for new search feature.

- refactor(creator-studio-section): improve layout and styling consistency

- Updated class names for better styling consistency across the component.
- Enhanced the layout structure for improved readability and visual appeal.
- Integrated Saudi Riyal icon for revenue display.
- Commented out unused locale handling code for potential future use.

- feat(company-profile): implement multilingual company profile page

- Created a shared CompanyProfilePage component for consistent layout across languages.
- Added Arabic, English, and Spanish versions of the company profile page.
- Introduced a new PDF design for the company profile, enhancing visual presentation.
- Developed HTML structure for bilingual slides, improving accessibility and usability.
- Implemented CSS styles for print and screen display, ensuring a cohesive design.

- Company profile (#266)

- feat(statsig): integrate Statsig client for enhanced feature management

- Added @statsig/js-client and updated StatsigProvider to utilize the new client.
- Implemented singleton pattern for StatsigClient to optimize performance.
- Updated various sections to replace Chip components with styled spans for better UI consistency.
- Introduced new business card components and print functionality for user profiles.
- Added multiple business card designs and associated assets for improved branding.

- feat(company-collateral): add company workspace and business card features

- Introduced a new Company workspace layout for managing company-related tasks.
- Implemented business card generation functionality, allowing users to create and print business cards.
- Added a dedicated page for company collateral, including links to various assets.
- Created a letterhead component for generating printable letterhead documents.
- Enhanced user authentication checks for accessing company-related features.

- feat(settings): enhance user settings interface and functionality

- Introduced new animations for shiny text and gradient backgrounds in global styles.
- Refactored settings pages to improve layout and consistency, including the addition of a new Settings UI component.
- Updated the profile, privacy, and billing settings pages to utilize the new UI components for better organization and readability.
- Removed unused imports and animations to streamline the codebase.
- Improved navigation and user experience across settings sections.

- feat(profile): enhance portfolio settings and user experience

- Replaced ProfileSettings component with PortfolioSettings for better portfolio management.
- Added functionality to manage user experience entries, including company, title, dates, and summaries.
- Implemented social link normalization and validation for user profiles.
- Updated internationalization files to include new terms related to companies and experiences.
- Refactored profile settings to streamline code and improve maintainability.

- refactor(creator-layout): migrate from CreatorLayoutV2 to CreatorLayout and update color tokens

- Replaced instances of CreatorLayoutV2 with CreatorLayout across multiple components for consistency.
- Updated color references from hardcoded violet/purple to primary color tokens in relevant files.
- Introduced a new CreatorFooter component for enhanced layout and navigation in the creator section.
- Improved overall code organization and maintainability by consolidating layout components.

---

### 2026-04-27

#### Add architecture documentation and update MCP server settings

- Introduced a comprehensive architecture document for the Experts App, detailing the system's structure, functional areas, execution flows, and notable observations.

- Added a new settings.json file for Claude configuration, specifying permissions and MCP server commands.
- Updated the settings.local.json for the experts-app to correct the command for the MCP_DOCKER server.

These changes enhance project documentation and improve configuration for better integration with development tools.

####

### 2026-04-26

#### Add graphify output and ignore files for experts-app

- Introduced `.graphifyignore` files to exclude generated and dependency files from the graph analysis.
- Updated `.gitignore` to include `graphify-out/cache` for better management of generated files.
- Added `graph.json`, `graph.html`, and `GRAPH_REPORT.md` to `graphify-out` directory for visualizing and reporting on the code structure.
- Implemented `graphify.py` script to automate graph generation and export to HTML format.
- Enhanced the overall project structure for better integration of graph analysis tools.

#### Update documentation and configuration for GitNexus integration

- Added GitNexus guidelines and best practices to AGENTS.md and CLAUDE.md for improved code intelligence and impact analysis.
- Introduced new .gitignore entries to exclude GitNexus-related files and CodeGraph data files.
- Created configuration files for CodeGraph to manage file inclusions and exclusions effectively.
- Enabled additional plugins in the cursor settings for enhanced functionality.

These changes enhance the project's documentation and configuration for better integration with code analysis tools.

#### Update GitNexus project indexing and enhance MCP server configuration

- Adjusted the GitNexus project indexing details in AGENTS.md and CLAUDE.md to reflect the current symbol and relationship counts.
- Removed the obsolete codegraph.lock file to streamline project dependencies.
- Updated the settings.local.json for the experts-app to enable all MCP servers and configure specific commands for GitNexus and CodeGraph, improving integration with code analysis tools.

These changes enhance the project's documentation and configuration for better code intelligence and server management.

#### Update GitNexus configuration and enhance project documentation

- Added new entries to .gitignore and .graphifyignore to exclude generated files and improve project cleanliness.
- Updated AGENTS.md and CLAUDE.md to reflect the latest symbol counts and provide clearer instructions for using GitNexus tools.
- Introduced new SKILL.md files for GitNexus CLI, debugging, exploring, impact analysis, and refactoring, enhancing user guidance for code management tasks.
- Removed obsolete graph output files from the experts-app to streamline the project structure.

These changes improve the project's documentation and configuration for better integration with GitNexus and overall code intelligence.

### 2026-04-22

#### Add attachment content API and access control

- Implemented a new API route for retrieving signed URLs for attachment content, allowing secure access to files.
- Created a validation schema for attachment ID and integrated authentication checks to ensure proper access control.
- Developed helper functions for building content disposition headers and managing attachment access based on user roles and course status.
- Added unit tests to verify the functionality of the new API route and access control logic, ensuring robust error handling for unauthorized access.

These changes enhance the security and usability of attachment management within the application.

### 2026-04-21

#### Refactor dashboard and lesson components for improved functionality and UI

- Streamlined imports in the dashboard page for better readability.
- Enhanced the dashboard to display course cards within a wrapper for consistent styling.
- Updated the `useVideoLessonCompletionGate` hook to include a new method for calculating maximum seekable position.
- Added support for various lesson types (text, PDF, audio, presentation) in the lesson player, improving content rendering.
- Introduced asset upload functionality in the course assets panel, allowing for better resource management.
- Enhanced lesson resource management with improved error handling and resource creation logic.

These changes collectively enhance the user experience by improving the layout, functionality, and accessibility of course and lesson components.

### 2026-04-20

#### Add Creator Studio Section and Mobile Token Reference

- Introduced the `CreatorStudioSection` component to the HomePage, enhancing the user interface with a dedicated section for creator tools.
- Added a new file `creator-studio-section.tsx` containing the layout and functionality for the Creator Studio.
- Created `mobile-tokens.md` to document design tokens for SwiftUI, ensuring consistency between web and mobile platforms.
- Updated the design system README to include references to the new mobile tokens documentation and additional slide templates for presentations.

#### Refactor HomePage and enhance lesson components with localization support

- Commented out the `CreatorStudioSection` in the HomePage for future use.
- Adjusted the `HeroSection` to use a calculated height for better responsiveness.
- Updated the `ValidationTracker` to improve padding for better visual clarity.
- Added localization labels for the portfolio section in `ProfileSettings`.
- Introduced lesson type components for text and video lessons, including localization for labels and placeholders in multiple languages.
- Enhanced the `CourseDetailsSection` and event forms with localized content labels for improved user experience.

### 2026-04-19

#### Enhance LearnPage and LessonPlayer with video lesson completion tracking

- Integrated a new `useVideoLessonCompletionGate` hook to manage video lesson progress and completion requirements.
- Updated `LessonPlayer` to utilize the video completion gate, ensuring users can only mark lessons as complete after watching required video content.
- Added a `CourseAssetsTab` component to display course assets, improving resource accessibility for learners.
- Enhanced `ModuleOverview` to include tabs for course overview and assets, streamlining navigation.
- Updated API routes for managing video watch progress, allowing for better tracking of user engagement with video lessons.

These changes collectively improve the learning experience by ensuring that video content is fully engaged with before marking lessons as complete, while also enhancing resource visibility.

### 2026-04-18

#### Enhance LearnPage and LessonPlayer components with improved navigation and UI

- Updated LearnPage to include a top navigation bar with links to dashboard, courses, and events, enhancing user accessibility.
- Integrated mobile responsiveness using the `useIsMobile` hook for better user experience on smaller screens.
- Refactored LessonPlayer to utilize new button variants for consistent styling.
- Added localization support for new navigation elements in English, Arabic, and Spanish.

These changes collectively improve the navigation and overall user experience within the learning platform.

#### Add environment configuration and enhance LearnPage functionality

- Introduced a new environment configuration file for the experts application.
- Updated LearnPage to utilize the `useRouter` hook for navigation, improving user experience.
- Enhanced loading state and lesson player components with better UI elements and loading indicators.
- Refactored lesson list and module overview sections for improved layout and accessibility.
- Implemented sidebar state management to persist user preferences across sessions.
- Enhanced LearnPage with better UI elements and loading indicators.
- Enhanced LearnerWorkspaceLayout with better UI elements and loading indicators.

These changes collectively enhance the overall functionality and user experience of the learning platform.

#### Update EventsClient header spacing and modify backup file naming in staging commands

- Increased margin for the header in EventsClient to improve layout.
- Renamed SQL backup file in staging commands for better clarity and consistency.

</details>

---

<details>
<summary><strong>[1.1.6] — 14-04-2026 - 2026-04-17</strong> — expand for full notes</summary>

<br />

[Google Docs V1.1.6](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?tab=t.l0gusvlyetr)

### 2026-04-17

> [!NOTE]
> RELEASE CANDIDATE

#### Update TypeScript configuration and enhance various components

- Updated `tsconfig.json` to exclude additional directories: `src/generated/**` and `coverage/**`.
- Modified `MarkdownPreviewComponent` usage in `ConsoleChangelogPage` to remove unnecessary `dir` prop.
- Added `type` field to `proofOfExpertise` in the certifications overview test.
- Included language parameter in the needs info checkpoint test.
- Removed unused `userId` from several certification queue tests.
- Updated `AdminPaymentsPage` to simplify `Tabs.List` component.
- Changed `entityLabel` to `entityType` in clone dialog components for better clarity.
- Enhanced error handling and user feedback in error components.
- Refactored various UI components to improve styling and usability.
- Added new localization messages for lifecycle actions in creator components.
- Fixed all type errors in the codebase.

These changes improve the overall structure, usability, and localization of the application.

#### Enhance curriculum management with course asset features

- Introduced CourseAssetsPanel for managing course-level assets, allowing users to add, upload, and remove various asset types (images, videos, files, links).
- Updated CurriculumBuilderShell to integrate the new CourseAssetsPanel, providing a dedicated section for managing course materials.
- Enhanced state management for curriculum components to support asset handling, including improved error handling and user feedback during asset uploads.
- Refactored existing curriculum logic to accommodate new asset functionalities, ensuring a seamless user experience.

These changes significantly improve the curriculum management capabilities, offering a more robust and user-friendly interface for handling course assets.

#### Implement question asset uploader and enhance exam/quiz dialogs

- Introduced the QuestionAssetUploader component for managing image and file uploads within exam and quiz dialogs.
- Updated ExamDialog and QuizDialog to utilize the new uploader, improving the user experience for adding assets to questions.
- Added error handling and localization for asset upload failures, enhancing feedback for users.
- Refactored existing file upload logic to streamline the process and improve maintainability.

These changes significantly enhance the functionality and usability of the exam and quiz management features within the curriculum.

#### Refactor exam management and enhance curriculum features

- Updated the curriculum management components to include improved error handling for exam creation and editing, ensuring better user feedback.
- Introduced new state management for exam-related actions, including error messages and form reset functionality.
- Enhanced localization for exam reporting and error messages, improving accessibility across multiple languages.
- Refined the user interface for exam dialogs, providing clearer feedback and improved usability.

These changes significantly enhance the exam management capabilities within the curriculum, offering a more robust and user-friendly experience.

#### Refactor curriculum management and enhance quiz functionality

- Updated quiz form validation to support multi-select question types, ensuring at least two correct options are required for such questions.
- Improved the curriculum management interface by refining the useCurriculum hook and related components for better state handling and user experience.
- Enhanced unit tests to cover new validation rules for multi-select questions, ensuring robust functionality.
- added new quiz question type: multi-select, full guide <https://github.com/logi-x/brain/blob/main/Raw/sources/2026-04-17-experts-question-types-plan.md>

These changes significantly improve the quiz management capabilities within the curriculum, providing a more flexible and user-friendly experience.

#### feat(curriculum): implement course exam management features

- Added functionality for creating, editing, and managing course exams within the curriculum.
- Introduced ExamDialog for exam creation and editing, replacing the previous ExamStubDialog.
- Updated curriculum management components to support exam-related actions and state management.
- Enhanced localization for exam-related features, ensuring accessibility across multiple languages.

These changes significantly improve the curriculum management interface by integrating comprehensive exam capabilities.

### 2026-04-16

#### Enhance Audio Features and Curriculum Management

- Added support for audio voice notes in the LessonDialog, allowing users to record and upload audio directly.
- Introduced the AudioRecorder and AudioWavePlayer components for seamless audio recording and playback.
- Updated the MarkdownEditor to include a voice note button, enabling easy integration of audio content.
- Enhanced the upload API to support audio file types, improving the media handling capabilities.
- Refactored curriculum components to incorporate drag-and-drop functionality for better organization of lessons and quizzes.

These changes significantly improve the user experience by providing new audio features and enhancing the overall curriculum management interface.

#### Refactor Curriculum Page and Enhance Lesson Management Features

- Removed unused state and effects in the CurriculumPage component to streamline logic and improve performance.
- Introduced a new effectiveSelectedModuleId state to simplify module selection logic.
- Updated lesson and quiz addition functions to utilize the new state, enhancing user experience.
- Improved localization support across various components, ensuring better accessibility for users.
- Refactored curriculum-related components for better organization and maintainability.

These changes significantly enhance the usability and performance of the curriculum management interface, providing a more efficient workflow for course creators.

#### Refactor Lesson Dialog and Markdown Editor for Improved Usability

- Enhanced the LessonDialog component by restructuring layout elements for better spacing and organization, including the introduction of NumberField for lesson duration input.
- Updated the MarkdownEditor to include a tooltip indicating Markdown support and added a description prop for better user guidance.
- Improved localization by removing "Markdown" from content labels in multiple languages for clarity.

These changes significantly enhance the user experience by providing clearer input structures and improved guidance within the application.

#### Refactor Environment Variables and Introduce AI Suggestion Features

- Updated environment files to secure sensitive information by
  commenting out the OPENAI_SECRET.
- Added new AI suggestion components, including AiSuggestButton and
  AiSuggestListButton, to enhance user interaction with AI-generated
  content.
- Implemented hooks for AI question generation and suggestions,
  improving the learning experience by providing automated content
  creation tools.
- Enhanced localization support for AI-related features, ensuring a
  better user experience across different languages.

These changes significantly improve the application's functionality by
integrating AI tools that assist users in content creation and
management.

#### Refactor Environment Variables and Introduce AI Suggestion Features

- Updated environment files to secure sensitive information by commenting out the OPENAI_SECRET.
- Added new AI suggestion components, including AiSuggestButton and AiSuggestListButton, to enhance user interaction with AI-generated content.
- Implemented hooks for AI question generation and suggestions, improving the learning experience by providing automated content creation tools.
- Enhanced localization support for AI-related features, ensuring a better user experience across different languages.

#### Enhance Home Page and Statistics with Event Data Integration

- Added totalEvents to the HomePage statistics, improving the visibility of event-related metrics.
- Updated the StatsSection to include totalEvents, enhancing the overall statistics display.
- Refactored CoursesSection and EventsSection to improve layout and user experience, including new messaging for empty states.
- Adjusted styling for various components to ensure consistency and improved aesthetics across the application.

These changes significantly enhance the user experience by providing clearer insights into event statistics and improving the overall layout of the home page sections.

### 2026-04-15

#### Assess and prepare for staging

## 1. App Readiness — Soft Launch & Aggressive Staging

### Assessment

Based on a technical audit of the codebase at `/experts/apps/experts-app` (conducted alongside this meeting), the platform is **substantially complete** at the infrastructure and feature level. A full implementation exists for:

- Instructor Certification (v1.0) — application, review, badge, email, revocation ✅
- Gated certification tiers (VERIFIED, ACADEMIC) ✅
- Payment infrastructure (Noon primary, Stripe backup, Tabby BNPL) ✅
- UI system on HeroUI ✅
- Auth (NextAuth v5, Google, Apple OAuth) ✅
- Subscription billing infrastructure ✅
- Course and Events modules (code exists; certification-gated publishing in progress) ✅
- Admin console, RBAC, analytics ✅
- i18n (Arabic, English, Spanish, RTL) ✅
- ZATCA e-invoicing ✅
- Docker containerisation and staging environment ✅

### Verdict

| Mode                           | Status                  | Condition                                                                                                                                         |
| ------------------------------ | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Aggressive staging testing** | **Ready now**           | Fix `typescript: { ignoreBuildErrors: true }` in `next.config.ts`; tighten image `remotePatterns`; audit Phase-13 Noon webhook TODOs              |
| **Soft launch (limited beta)** | **Ready in ~2–3 weeks** | Complete certification-gated course publishing (Phase 8–9), connect subscription access gating to course access, confirm staging smoke tests pass |

### Critical remaining items before soft launch

1. **Courses module publishing gate** — course publish workflow needs to be gated by instructor certification level (Phase 8–9). Code exists; logic not fully wired.
2. **Subscription access gating** — infrastructure is done; access control at course/content level needs finalising.
3. **Events module** — base code exists; confirmation needed that location, capacity, and refund policy flows are complete.
4. **Client-side blockers (Adnan):** logo/brand assets, category list, 1 sample course, instructor ToS draft — all still open from November 2025.

---

## 2. Approximate Launch Date

**Soft launch target remains mid-July 2026**, consistent with the November 2025 decision.

- Current milestone v1.1 (certification depth, Phase 7–9) is on track to complete by end of May.
- That leaves 6 weeks for staging, QA, content seeding, and go-live prep.
- Dedicated server provisioning to be initiated ~4 weeks before launch.
- Ahmed Sulaimani confirmed sharing an updated project timeline with the group (completing today per agenda).

**Risk flag:** Client-side blockers (logo assets, categories, sample course, ToS) remain open since November — these must be resolved by end of April to avoid slipping the July window.

---

## 3. Marketing Plan — Adnan Ishgi

> _No transcript available. Summary to be filled in by attendee._

Topics expected to have been covered:

- Channel strategy for Experts platform launch (social, email, direct outreach to instructors)
- Target audience segmentation for the Saudi market
- Partnership or co-marketing with content providers (e.g. Samaya)
- Timeline for marketing activities relative to soft launch
- Budget allocation

### 2026-04-14

#### Enhance Learning Experience with Curriculum Item View State Management

- Introduced a new view model for managing curriculum item states, including accessibility, completion status, and unlock reasons.
- Refactored the `useCoursePlayer` hook to utilize the new view model, improving state management for lessons and quizzes.
- Updated components such as `LessonList`, `LessonPlayer`, and `ModuleOverview` to leverage the new view state, enhancing user interaction with up-next and resume features.
- Added resource handling in `LessonPlayer` to display downloadable materials and links effectively.

These changes significantly improve the learning experience by providing clearer visibility into lesson accessibility and progress tracking.

#### Update Course Type and Refactor Course Player Logic

- Added the "instructors" field to the Course type definition to enhance course data structure.
- Refactored the useCoursePlayer hook to directly type course data as Course, improving type safety and clarity.
- Streamlined instructor role checking logic for better readability.

These changes improve the data model and enhance the functionality of the course player, contributing to a more robust learning experience.

#### Implement Course Player and Enhance Learning Experience

- Introduced a new `useCoursePlayer` hook to manage course state, including lesson progress and module selection.
- Added several components for the learning interface, including `CertModal`, `LessonList`, `LessonPlayer`, and `ModuleOverview`, to improve user interaction and content accessibility.
- Enhanced loading states and progress tracking with new `LoadingState` and `ProgressCard` components.
- Refactored existing components to streamline the layout and improve the overall user experience in the learning environment.

These changes significantly enhance the functionality and usability of the course learning experience, providing a more engaging and organized interface for users.

#### Refactor Learn Page and Introduce Learner Workspace Components

- Integrated LearnerWorkspaceLayout and LearnerWorkspaceToolbar to enhance the structure of the LearnPage component.
- Updated type definitions for Course, LessonProgress, and related entities to improve type safety and clarity.
- Removed redundant type definitions and imports to streamline the codebase.
- Enhanced the layout and user experience by implementing a more cohesive header and sidebar structure.

These changes improve the organization and usability of the learning interface, providing a better experience for users navigating course content.

#### Refactor Course and Event Components for Improved Structure and Validation

- Removed unnecessary padding from Card.Content in CourseOverviewPage and EditCoursePage for a cleaner layout.
- Updated EventOverviewPage to enhance the structure of the completion section, integrating a ProgressBar for better visual feedback.
- Introduced a new ValidationTracker component to display validation issues in CourseForm, ensuring users are informed of required fields.
- Deleted outdated CourseCardV2 and EventCardV2 components to streamline the codebase and improve maintainability.

These changes enhance the user experience by providing clearer validation feedback and a more cohesive layout across course and event components.

#### Update global styles and component structures for improved consistency and usability

- Adjusted CSS variables for muted colors and surfaces to enhance visual consistency across the application.
- Updated the testimonials section to use the new muted-foreground color for better integration with the design system.
- Refined the courses and events components by modifying border styles and enhancing layout elements for a more cohesive user experience.
- Improved event form validation to ensure proper pricing requirements are enforced based on user selections.

These changes enhance the overall aesthetic and functionality of the application, providing a more streamlined user experience.

#### Enhance Claude Code Skills Documentation and Introduce New Skills

- Added detailed sections for Claude Code skills in AGENTS.md and CLAUDE.md, outlining the usage and paths for **experts-ecosystem**, **experts-orbit**, and **experts-cosmos**.
- Created new documentation files for **experts-claude-skills.mdc** and **experts-ecosystem-skill-sync.mdc** to guide when to update skill playbooks based on coding conventions and structural changes.
- Updated existing documentation to clarify the relationship between skills and their respective usage contexts, ensuring accurate guidance for developers.
- Introduced new skills for workspace shell design and native app implementation, enhancing the overall developer experience and project consistency.

These changes improve the clarity and usability of the documentation, ensuring that developers have the necessary resources to maintain and implement coding standards effectively.

#### Update version to 1.1.6 and add brain vault documentation

- Bumped package versions in package.json files for @logi-x/experts, @logi-x/experts-app, and @logi-x/experts-app-worker to 1.1.6.
- Introduced new brain-vault-obsidian.mdc file for documenting the brain vault usage and session-close guidelines.
- Updated experts-rule-guide.mdc to include a reference to the new brain vault documentation.
- Adjusted environment files to reflect the new app version.

These changes enhance version tracking and provide essential documentation for project memory and decision-making processes.

</details>

<details>
<summary><strong>[1.1.5] — 26-03-2026 - 14-04-2026</strong> — expand for full notes</summary>

<br />

[Google Docs V1.1.5](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?pli=1&tab=t.yq3ot18bfy8z)

### 2026-04-14

> [!NOTE]
> RELEASE CANDIDATE

#### Refactor AdminShell and introduce AdminWorkspaceShell for enhanced layout and user profile integration

- Updated AdminShell to accept a profile prop, allowing for user information display within the admin interface.
- Introduced AdminWorkspaceShell to manage sidebar navigation and layout, grouping navigation items for better organization.
- Enhanced navigation items with grouping labels for improved clarity and user experience.

These changes improve the overall structure and usability of the admin interface, providing a more cohesive user experience.

#### Refactor Admin UI components and update global styles for improved consistency

- Introduced new AdminHeader and AdminSidebar components to enhance the admin interface layout and user experience.
- Updated AdminWorkspaceShell to integrate the new header and sidebar, improving navigation and organization.
- Modified global CSS variables for background and sidebar colors to ensure a cohesive design across the application.
- Adjusted NavbarV2 to utilize the updated sidebar color scheme for better visual alignment.

These changes enhance the overall usability and aesthetic of the admin interface, providing a more streamlined user experience.

#### Refactor Admin Navigation Components for Enhanced Structure and Usability

- Introduced new components for the admin sidebar navigation, including AdminNavMain, AdminNavProjects, AdminNavSecondary, and AdminNavUser, to improve organization and user experience.
- Updated AdminSidebar to utilize the new navigation components, streamlining the sidebar structure.
- Enhanced AdminWorkspaceShell to integrate the updated sidebar and breadcrumb navigation for better layout and accessibility.
- Adjusted NavbarV2 for improved visual consistency with the updated sidebar color scheme.

These changes enhance the overall usability and aesthetic of the admin interface, providing a more streamlined user experience.

#### Update global styles and component backgrounds for consistency

- Added a new CSS variable for background color and updated existing components to use this variable for a cohesive design.
- Replaced instances of 'bg-background' with 'bg-bg' across various components to ensure uniformity in background styling.
- Enhanced the overall visual consistency of the application by aligning background colors with the new design system.
- update-packages

These changes improve the aesthetic and usability of the application, providing a more streamlined user experience.

### 2026-04-13

#### Enhance Documentation and Update Dependencies

- Updated AGENTS.md and CLAUDE.md to emphasize the importance of the brain vault for project memory and decision tracking, including new session close guidelines for capturing knowledge.
- Improved context order in documentation for clarity on using Obsidian notes and Graphify outputs.
- Updated package.json and pnpm-lock.yaml to reflect new versions of devDependencies, including @types/node, baseline-browser-mapping, and prettier for improved development experience.
- Introduced new AdminNavbar component and refactored existing admin components for better organization and usability in the admin interface.

These changes improve documentation clarity and ensure the application is using the latest dependencies for optimal performance.

#### Refactor Admin Components and Introduce AdminNavbar

- Removed the SidebarToggleButton from AdminHeader to streamline the component.
- Introduced a new AdminNavbar component to enhance the admin interface with improved navigation and user interaction features.
- Updated AdminWorkspaceShell to integrate AdminNavbar and manage sidebar state more effectively.
- Enhanced AdminSidebar to support RTL layout adjustments based on user preferences.

These changes improve the organization and usability of the admin interface, providing a more cohesive user experience.

### 2026-04-12

#### Update package-lock.json and docker-compose.yml for dependency management and service configuration

- Added 'vitest' as a new dependency in package-lock.json for improved testing capabilities.
- Updated dependencies for '@emnapi/core', '@emnapi/runtime', and '@emnapi/wasi-threads' to version 1.9.2.
- Changed Redis service port mapping in docker-compose.yml from 6379:6379 to 6380:6379 for better port management.
- Ensured proper formatting and consistency in docker-compose.yml by removing unnecessary whitespace.

These changes enhance the testing framework and improve service configuration in the application.

#### Refactor AppEnvironmentStore to validate local base URLs and update related tests

- Enhanced AppEnvironmentStore to reject non-absolute local URLs, defaulting to a fallback URL when necessary.
- Updated APIClientDecodingTests to check for URL prefix instead of exact match for better flexibility.
- Adjusted StorePersistenceTests to verify base URL behavior with invalid local URL strings.

These changes improve URL handling and testing robustness in the application.

### 2026-04-11

#### Update community thumbnail source and add new planning summaries

- Replaced the community thumbnail fallback image with a stable Unsplash URL for better alignment with the native card layout.
- Introduced new planning summaries for the "Bring App to Life" phase, detailing results, verification steps, and open risks for each plan.
- Added configuration file for workflow management in the planning directory.

#### Enhance AsyncRemoteImage and ContentListCard for improved layout and … (#248)

…placeholder handling

- Updated AsyncRemoteImage to enforce a minimum height, ensuring
  consistent display across varying image aspect ratios.
- Refactored placeholder handling in AsyncRemoteImage to use a dedicated
  view, improving code clarity and maintainability.
- Adjusted ContentListCard to ensure the AsyncRemoteImage fills the
  available width and clips correctly, preventing layout issues.

#### Refactor AGENTS.md and introduce CLAUDE.md for improved project navig… (#247)

…ation

- Updated AGENTS.md to serve as the routing index for agent work in the
  Experts app, streamlining context order and non-negotiables.
- Added CLAUDE.md as a new routing index for agent context at the
  repository root, emphasizing minimal context usage and project memory
  practices.
- Removed outdated sections and consolidated repository commands and
  conventions into new dedicated files for better organization.

These changes enhance clarity and accessibility of project guidelines,
improving developer onboarding and workflow.

#### Add forgot password and registration routes with tests (#246)

- Implemented POST routes for user password reset and registration,
  including validation and error handling.
- Added unit tests for both routes to ensure proper functionality and
  edge case handling.
- Integrated notification service for sending password reset emails and
  ensured secure user enumeration prevention.
- Established user account creation logic with password hashing and
  subscription management.

These changes enhance the authentication flow and user management
capabilities in the application.

#### Enhance AsyncRemoteImage and ContentListCard for improved layout and placeholder handling

- Updated AsyncRemoteImage to enforce a minimum height, ensuring consistent display across varying image aspect ratios.
- Refactored placeholder handling in AsyncRemoteImage to use a dedicated view, improving code clarity and maintainability.
- Adjusted ContentListCard to ensure the AsyncRemoteImage fills the available width and clips correctly, preventing layout issues.

#### Enhance error handling and debugging information in APIClient and StateViews

- Added optional failure class label to ErrorStateView for better debugging in DEBUG builds.
- Improved error messages in APIClient to include endpoint paths for easier traceability of server and decoding errors during development.
- Introduced DecodingContextError to provide clearer diagnostics for decoding failures.
- Updated localized error messages in English, Arabic, and Spanish for unauthorized access, not found, and server errors.

#### Add forgot password and registration routes with tests

- Implemented POST routes for user password reset and registration, including validation and error handling.
- Added unit tests for both routes to ensure proper functionality and edge case handling.
- Integrated notification service for sending password reset emails and ensured secure user enumeration prevention.
- Established user account creation logic with password hashing and subscription management.

These changes enhance the authentication flow and user management capabilities in the application.

#### feat(01-03): add local environment diagnostics card in profile

- New LocalDiagnosticsView shows effective base URL and API v1 path in DEBUG builds
- Card visible only when environment is set to local
- Includes simulator vs physical device connectivity hints
- Localized in English, Arabic, and Spanish

#### Refactor AGENTS.md and introduce CLAUDE.md for improved project navigation

- Updated AGENTS.md to serve as the routing index for agent work in the Experts app, streamlining context order and non-negotiables.
- Added CLAUDE.md as a new routing index for agent context at the repository root, emphasizing minimal context usage and project memory practices.
- Removed outdated sections and consolidated repository commands and conventions into new dedicated files for better organization.

These changes enhance clarity and accessibility of project guidelines, improving developer onboarding and workflow.

### 2026-04-10

#### No major changes

### 2026-04-09

#### Implement enhanced error handling for payment capture and invoice generation

- Introduced a new error class, PaymentCapturedInvoiceError, to handle cases where payment is successfully captured but invoice generation fails.
- Updated the event registration flow to throw this error when invoice creation fails, ensuring users receive appropriate feedback.
- Enhanced UI to display specific messages for payment capture issues, improving user experience during payment processing.
- Added unit tests to cover scenarios where invoice generation fails after payment capture, ensuring reliability in error handling.

### 2026-04-08

#### Enhance payment flow error handling and UI feedback

- Updated payment confirmation messages to provide clearer user feedback in case of errors during e-invoice generation.
- Improved error handling for unique constraint violations related to invoice numbers.
- Refactored various components to ensure consistent error messaging and user experience across the application.
- Added unit tests for edge cases in payment processing to enhance reliability.

#### Refactor follow list types and improve generic handling

- Updated FollowListUser type to FollowListUserBase for better extensibility.
- Enhanced FollowListResponse to support generics, allowing for more flexible user data handling.
- Modified optimisticPatch function to utilize generics for improved type safety.
- Adjusted useFollowListRow hook to accommodate the new generic types, ensuring consistent type management across follow list functionalities.

#### Refactor follow functionality and enhance user experience

- Updated the UserProfileShell, FollowersPage, and FollowingPage components to utilize a new useFollowListRow hook for managing follow actions.
- Improved follow button feedback with pending states and loading indicators to enhance user experience during follow/unfollow actions.
- Refactored follow logic to handle asynchronous operations more effectively, ensuring UI updates reflect the current state accurately.
- Added presence indicators to user lists for better visibility of online status.
- Cleaned up code and improved readability across affected files.

#### Enhance presence management and user experience

- Refactored presence handling to improve online/offline state detection and user experience.
- Updated presence caching logic to include long-TTL last-seen timestamps for offline users.
- Improved the PresenceIndicator component to accurately reflect user states (online, away, offline) with tooltips.
- Removed deprecated leave endpoint and adjusted heartbeat logic for better performance.
- Enhanced usePresence hook to manage tab visibility and network events for more reliable presence tracking.
- Cleaned up redundant comments and improved code readability across presence-related files.

#### Web/feature/realtime ws keepalive (#242)

- fix(realtime): WebSocket ping keepalive and stable useRealtime deps

- experts-realtime: periodic ws.ping() (WS_PING_INTERVAL_MS, default 25s) to beat proxy idle timeouts
- useRealtime: channel set keyed by sorted join + refs for channels/options to avoid resubscribe churn
- Document keep-alive and JWT handshake in realtime-contract + experts-realtime README

- feat(realtime): dynamic WS subscribe/unsubscribe without reconnect

- experts-realtime: mutable Redis subscription, sanitize channels on subscribe (mirror channel-auth)
- Allow authenticated handshake with empty JWT channels; session token TTL 24h
- Client: fetchConnectionToken tries empty body first; scheduleChannelSync sends op messages
- Token route: signed-in empty channels mints dynamicChannels session JWT
- Docs + README; deprecate scheduleReconnectForChannelChange alias

- feat(realtime): pong liveness, subscription acks, graceful offline

- Track pong after server ping; close half-open sockets (WS_PONG_LIVENESS)
- Redis INCR/DECR per user open sockets; markGlobalOffline after grace if still zero
- subscription_ack envelopes for subscribe/unsubscribe (sanitize/cap/redis errors)
- Extract subscription-plan pure logic + Vitest; exclude tests from tsc emit
- Document presence vs ping, acks, grace, JWT tradeoff in contract + README

- refactor(realtime): viewer_join/leave as primary path, sync as reconcile

- PresenceCoordinator: ref-count scopes per tabId; incremental WS join/leave
- viewer_sync + HTTP only after handoff, WS reconnect, visibility resume, or WS send failure
- BroadcastChannel request_scopes so new leader rebuilds aggregate before reconcile
- Global coordinator: trySendViewerJoinWs/LeaveWs, registerViewerPresenceReconcile on socket open

- fix(realtime): retry WS when session/channels arrive after first connect attempt

- WebSocketTransport.kickConnect: reset reconnect backoff and reconnect (start() is no-op once started)
- Global coordinator: ensureLeaderWebSocket on channel updates and auth; remove duplicate init connect
- AuthProvider: notifyAuthMayHaveChanged when NextAuth status leaves loading
- Mock kickConnect delegates to wsStart in tests

- feat(realtime): enhance presence management and connection token handling

- Added environment variables for E2E testing to support real-time features.
- Updated view tracking logic to trigger on page entry without engagement thresholds.
- Refactored presence hooks to ensure user ID checks are more robust.
- Introduced caching for real-time connection tokens to reduce redundant fetches and improve performance.
- Implemented visibility change handling to reconnect WebSocket after long background periods.

#### feat: implement minimal production-ready seeded data and legacy migration support

- Added a new script for minimal production-ready seeded data to ensure the application operates correctly with essential data.
- Introduced legacy migration scripts to facilitate the transition from MySQL to PostgreSQL, including detailed mapping and data handling.
- Updated package.json to include new database seed commands for minimal and legacy data imports.
- Enhanced event mapping functions to improve data handling and scheduling logic.
- Added tests for legacy migration functions to ensure data integrity during the migration process.

### 2026-04-07

#### feat: add SQL script for missing data migration

- Introduced a new SQL script to handle the migration of missing data, including the creation of `attachments`, `coupons`, and `course_coupon` tables.
- The script includes necessary foreign key constraints and initial data insertion for attachments.
- This addition aims to improve data integrity and facilitate the migration process for future updates.

#### style: update global styles and Navbar component

- Added styles for the .wmde-markdown class to ensure consistent font settings.
- Adjusted Navbar component's Dropdown.Trigger to use min-height and min-width for better layout consistency.
- Enhanced MarkdownPreview component by updating regex patterns to support periods in mentions and hashtags, and added overflow styling for improved text handling.

#### feat: enhance MentionLink component with link disabling option

- Added a `disableLinks` prop to the MentionLink component to conditionally render mentions as plain text instead of links.
- Updated the regex to support periods in usernames.
- Modified the TimelineActivityItem to pass the `disableLinks` prop based on the presence of an activity link, improving user experience and preventing nested link issues.

#### refactor: enhance TimelineActivityItem interactivity

- Replaced the Link component with a div to handle click events for activity links, improving accessibility and preventing hydration errors.
- Implemented custom navigation logic using useRouter for better routing control.
- Added keyboard navigation support for accessibility compliance.

#### Fix enrollment and registration badges for pending payments. (#241)

- Only treat course enrollments and event registrations as active when the record status is completed, so cards do not show Enrolled/Registered for incomplete payments.

#### refactor: update AuthProvider to manage profile fetching with local state

- Replaced the useApiQuery for profile fetching with local state management in AuthProvider.
- Introduced useState for profile and loading state, and implemented a fetchProfile function to handle API calls.
- Updated useEffect to call fetchProfile based on session changes, improving the handling of user profile data.

#### refactor: migrate client fetching to useApiQuery (#240)

Replace direct SWR and effect-based GET fetches with useApiQuery across
key pages and hooks to unify auth-aware caching and revalidation
behavior.

#### refactor: migrate client fetching to useApiQuery

Replace direct SWR and effect-based GET fetches with useApiQuery across key pages and hooks to unify auth-aware caching and revalidation behavior.

#### chore: update to-do list with user password algorithm notes and data extraction details

- Modified the to-do list to include a note about potentially adding password algorithm detection for users, emphasizing the need for users to reset their passwords if using an outdated algorithm.
- Added a reference to the source of old data extraction from a specific SQL file path.

#### chore: remove old migration scripts and related files

- Deleted outdated migration scripts for migrating old MySQL data to PostgreSQL, including `migrate-experts-old-data.ts`, `migrate-howa-old-data.ts`, and associated SQL files.
- Removed the `upgrade-guide.md` and data transformation utilities that are no longer needed.
- Cleared out old seeder files and documentation related to the previous migration process to streamline the codebase.

#### chore: update staging environment configuration and WebSocket handling

- Changed NEXT_PUBLIC_REALTIME_WS_URL to use a secure WebSocket URL for the staging environment.
- Added REALTIME_WS_SECRET to the staging environment variables for enhanced security.
- Updated server.ts to include type annotations for WebSocket message handling, improving type safety.

#### feat: add WebSocket support and enhance staging configuration

- Introduced NEXT_PUBLIC_REALTIME_WS_URL for real-time WebSocket connections in staging environment.
- Updated docker-compose.yml to include environment variables for Redis configuration and added Traefik labels for routing.
- Enhanced CHANGELOG.md with detailed notes on recent features, including hybrid WebSocket integration and real-time event publishing.

#### docs: enhance SKILL.md for Experts ecosystem with absolute path instructions

- Updated documentation to clarify the use of absolute paths for loading canonical docs and resolving `REPO_ROOT`.
- Added detailed steps for setting or discovering `REPO_ROOT` and clarified paths for various configurations.
- Improved sections on reading files and understanding the directory structure within the Experts monorepo.

#### feat: add hybrid WebSocket realtime with experts-realtime gateway

1- integrate presence updates with WebSocket and Redis pub/sub

- Added `publishPresenceUserUpdate` function to handle presence updates via Redis pub/sub.
- Updated presence routes to publish user presence changes on PUT and POST requests.
- Enhanced `usePresence` and `useUserPresence` hooks to manage real-time updates through WebSocket.
- Refactored presence caching logic to improve performance and reduce redundant requests.

2- enhance community interactions with real-time event publishing

- Added real-time event publishing for comment and post actions using Redis pub/sub.
- Implemented `publishFeedEvent` and `publishPostEvent` for comment additions, deletions, and post creations/updates.
- Updated API routes to invalidate caches and publish relevant events upon comment and post modifications.
- Enhanced hooks to handle new event types for better feed updates and notifications.

3- deprecate HTTP presence endpoints in favor of WebSocket integration

- Marked HTTP presence endpoints (`heartbeat`, `leave`, `sync`) as deprecated, indicating that the primary write path is now through WebSocket.
- Updated `usePresence` and `useScopedPresence` hooks to utilize the new global coordinator for presence management.
- Introduced a new `globalCoordinator` to handle WebSocket presence heartbeats and viewer sync operations.
- Added Redis-based presence management functions to support the new architecture.
- Enhanced the WebSocket server to handle presence-related messages and maintain user presence state.

4- implement viewer updates and optimize presence management

- Introduced `publishViewersUpdated` function to notify clients of changes in viewer counts for posts, courses, and events via Redis pub/sub.
- Enhanced presence management by ensuring users are removed from other scopes when joining a new one, with corresponding notifications sent to clients.
- Updated `useViewersSnapshot` and related hooks to leverage WebSocket for real-time updates, reducing reliance on polling.
- Refactored polling intervals and added a new utility for managing polling based on visibility state.
- Improved overall performance and responsiveness of viewer-related features in the application.

- Add realtime coordinator tests and test reset proxy for globalCoordinator

### 2026-04-06

No major changes.

### 2026-04-05

#### feat: enhance admin dashboard and UI components

- Introduced an AdminShell component for improved layout and navigation in the admin interface.
- Updated admin layout files to utilize the new AdminShell, enhancing consistency across different languages.
- Refactored dashboard components to improve structure and styling, including the OverviewCards and DashboardPanel.
- Added missing admin controls and ensured the use of correct HeroUI v3 components throughout the application.
- Replaced manual SWR usage with a centralized useApiQuery hook for data fetching consistency.
- Updated .gitignore to exclude generated documentation files.

</details>

---

<details>
<summary><strong>[1.1.4] — 2026-03-26 - 04-04-2026</strong> — expand for full notes</summary>

<br />

[Google Docs V1.1.4](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?pli=1&tab=t.troonsh9pz1k)

### 2026-04-04

> [!NOTE]
> RELEASE CANDIDATE

#### chore: update dependencies and improve UI components

- Bumped versions of several dependencies including AWS SDK, HeroUI, and others for better performance and security.
- Refactored CSS styles for improved list handling and modal backdrop layering.
- Updated the CoursesHeader component to use onPress instead of onClick for better accessibility.
- Enhanced Navbar and AuthPrompt components with improved layout and functionality.
- Added profile completion prompt translations for Arabic, English, and Spanish.

### 2026-04-03

#### refactor: update color scheme and improve UI consistency

- Replaced hardcoded violet/purple colors with primary token equivalents across multiple components for better consistency.
- Updated hex values for BRAND_PRIMARY_HEX in various files to reflect the new color scheme.
- Enhanced button and avatar styles to use the new color tokens, ensuring a cohesive look throughout the application.
- Added a .gitignore file for UI review screenshots to prevent committing binary assets.

#### feat: complete Phase 13 of Noon production hardening

- Marked Phase 13 as complete, finalizing the implementation of billing and payment status features.
- Updated the roadmap and state documentation to reflect the completion status and progress metrics.
- Added new summary files for completed plans, detailing accomplishments and key decisions made during the phase.
- Enhanced the admin payments UI with new components for monitoring failed webhooks, stuck checkouts, and active subscriptions.
- Implemented localization for the admin payments workspace, ensuring support for English, Arabic, and Spanish.
- Improved user experience with new subscription status labels and enhanced error handling in the billing settings page.

#### feat: implement admin payment monitoring and reconciliation features

- Introduced a new Vercel cron job for daily batch reconciliation of Noon subscriptions.
- Added admin APIs for monitoring failed webhooks, stuck checkouts, active subscriptions, and reconciliation logs.
- Implemented a shared admin payments UI with tabs for failed webhooks, stuck checkouts, active subscriptions, and reconciliation logs, utilizing the new backend APIs.
- Enhanced the reconciliation process with improved error handling and user notifications for subscription management.
- Updated documentation to reflect new features and UI components.

### 2026-04-02

#### feat: enhance payment status handling and localization

- Added a new payment status page to handle subscription verification and display appropriate messages for success and cancellation scenarios.
- Implemented localization for payment status messages in Arabic, English, and Spanish.
- Updated the subscription checkout handler to redirect to the new payment status page upon successful checkout.
- Enhanced test coverage for payment verification and subscription handling in various scenarios.

### 2026-04-01

#### feat: add end-to-end tests for Noon subscription checkout

- Introduced a comprehensive suite of end-to-end tests for the Noon subscription checkout process, covering various scenarios including pricing page UI, payment flows, and API edge cases.
- Implemented dedicated test users for consistent testing across different payment methods (VISA, Mastercard, mada).
- Enhanced the success page to handle payment cancellations and display appropriate messages.
- Updated configuration files to support new test commands and environments.

#### feat: implement retry logic for retrieving Noon orders by reference

- Enhanced the getNoonOrderByReference function to include a retry mechanism for network errors, allowing up to three attempts before throwing an error.
- Improved error handling to differentiate between network-related issues and other errors, ensuring more robust order retrieval.

#### feat: add NOON_MANAGEMENT_URL to environment files and update noon client configuration

- Introduced NOON_MANAGEMENT_URL in .env.e2e and .env.local for better management URL handling.
- Updated noon client to utilize NOON_MANAGEMENT_URL for constructing management URLs in subscription intents.
- Added a new verification report for phase 12 on Noon checkout metadata reliability, detailing human verification requirements and observable truths.

#### feat(12-02): replace Noon deep-search with DB-based metadata lookup in verify route

- Replace broken findStringValue/findEnumValue deep-search for plan metadata with prisma.noonPendingCheckout.findUnique lookup
- Return 400 with distinct error messages for not-found vs expired checkout sessions
- Delete NoonPendingCheckout row after successful metadata extraction
- Add fire-and-forget cleanup of expired sessions
- Remove unused findEnumValue function
- Retain findSubscriptionIdentifier/findNumberValue/findStringValue for Noon-native fields

#### feat(12-01): persist NoonPendingCheckout before redirect in createNoonSubscriptionIntent

- Import prisma singleton into noon gateway
- Create NoonPendingCheckout row after Noon API success, before returning redirect URL
- Store planCode, billingInterval, userId, planId, and 24h TTL expiresAt

#### feat(12-01): add NoonPendingCheckout Prisma model and migration

- Add NoonPendingCheckout model in billing schema with unique internalReference
- Include expiresAt index for TTL cleanup queries
- Migration creates noon_pending_checkouts table

### 2026-03-31

#### docs(11-01): complete noon subscription webhook handler plan

- Add 11-01-SUMMARY.md with execution results and decisions
- Update STATE.md: advance plan, update progress to 83%, add decisions, record session
- Update ROADMAP.md: mark phase 11 as Complete (1/1 plans)

#### feat(11-01): add subscription lifecycle handling to Noon webhook handler

- Extend NoonWebhookResult.target to include "subscription" union member
- Import handleSubscriptionRenew and handleSubscriptionCancel handlers
- Insert subscription lookup block BEFORE the enrollment failed-cancel path
- Renewal success: advances period by 30 days, calls handleSubscriptionRenew, logs observe, updates webhookEvent result to subscription_renewed
- Failed + Noon cancel signal (CANCEL in raw fields): calls handleSubscriptionCancel, updates webhookEvent result to subscription_canceled
- Failed + no cancel signal: sets subscription status to paused, updates webhookEvent result to subscription_payment_failed
- Cancellation detected via event.raw type/orderStatus/order.status fields, not event.status comparison
- Unrecognised subscription status falls through to existing unmatched_reference warn path

#### feat: enhance curriculum management and align with heroui components

- Updated the curriculum page to utilize CreatorLayoutV2 for improved aesthetics and functionality.
- Integrated new lesson types (PDF, Audio, Presentation) into the lesson dialog for better content variety.
- Enhanced lesson progress display with updated UI components from heroui, including Cards and ProgressBars.
- Improved RTL support and accessibility features across various curriculum sections.
- Refactored lesson handling logic to accommodate new media types and ensure consistent user experience.
- Added translation support for new lesson types and UI elements to enhance internationalization.

#### feat: integrate Noon Payments subscription handling and enhance pricing flow

- Updated the /pricing page to support Noon Payments as a subscription provider, allowing for dynamic provider resolution.
- Implemented subscription event handling in the Noon webhook to manage renewal, failure, and cancellation events.
- Enhanced the checkout verification route to accommodate Noon subscription metadata and ensure accurate subscription status updates.
- Added new functions for creating and retrieving Noon subscriptions, improving the overall payment integration.
- Conducted extensive research on Noon Payments to ensure a robust integration and address existing gaps in the subscription flow.

#### feat: implement end-to-end testing with Playwright and enhance test configurations

- Added Playwright for end-to-end testing, including setup for student and admin authentication.
- Created new test scripts and fixtures for role-based access control.
- Updated Playwright configuration to support multiple test projects and storage states.
- Introduced a README for E2E tests, detailing setup and common test runs.
- Enhanced environment configuration for testing with a dedicated .env.e2e file.
- Refactored existing scripts to accommodate new testing workflows and improved database migration commands.

### 2026-03-30

#### feat: add end-to-end testing setup with Playwright

- Introduced Playwright for end-to-end testing, enhancing test coverage and reliability.
- Added new scripts for running Playwright tests, including options for UI and debug modes.
- Created a Playwright configuration file to manage test settings and server behavior.
- Implemented mock data for public APIs to facilitate testing of various application routes.
- Developed initial smoke tests for key public routes to ensure proper rendering and functionality.

#### feat: enhance gallery functionality and improve RTL support

- Integrated a new Gallery component for displaying images in courses and events, allowing for better visual presentation.
- Updated course and event pages to utilize the Gallery component, enhancing user experience with image slideshows.
- Added support for right-to-left (RTL) layouts in the Gallery component and related UI elements.
- Improved localization messages for gallery interactions, ensuring clarity in multiple languages.
- Refactored CSS to maintain consistent styling across the new gallery features.

#### feat: enhance internationalization support and improve UI components

- Integrated appTimeZone into NextIntlClientProvider across various layout files for consistent timezone handling.
- Added EmptyState component for better user experience in course detail tabs when no content is available.
- Updated localization messages for improved clarity and consistency in multiple languages.
- Refactored QRCodeShare and ShareModal components to utilize translations for better accessibility.
- Enhanced global CSS to maintain consistent styling for list elements.

#### refactor: rename CourseFilterSidebar to CourseSidebarFilter and update imports

- Renamed the CourseFilterSidebar component to CourseSidebarFilter for consistency across the application.
- Updated all relevant imports and references to reflect the new component name.
- Ensured that the migration to HeroUI components is maintained throughout the affected files.
- Add Schedule Type to EventSidebarFilter and EventFiltersBar.

### 2026-03-29

#### refactor: unify description fields and enhance content structure

- Replaced 'shortDescription' with 'content' across courses and events for consistency.
- Updated related components and API routes to reflect the new content structure.
- Adjusted localization files to align with the new field names.
- Enhanced database schema to support the new content field for better data management.
- Replaced deprecated constants for title, description, content, and coupon code max lengths with references to CONFIG.
- Enhanced consistency and maintainability by centralizing configuration values in the shared config module.

#### feat: update routing and enhance markdown editor

- Added new routes for /changelog and /reports in the proxy configuration.
- Refactored ConsoleChangelogPage to fetch changelog from /reports/CHANGELOG.md.
- Improved MarkdownEditor with additional props for error handling and required fields.
- Updated styling and structure in MarkdownPreview and various form components for better user experience.

#### feat: add console changelog page with markdown reader

- Added /console/changelog route (shared + en/ar/es locale wrappers)
- Renders `reports/CHANGELOG.md` via MarkdownPreviewComponent
- Hero section with violet gradient, consistent with console/status style
- Fetches markdown client-side with loading skeleton and error state (pure HeroUI)
- Added changelog nav link to console and status page headers
- Added translations for changelog keys (EN/AR/ES)

#### feat: update app version and enhance console status page

- Bumped app version from 1.1.3 to 1.1.4 in the staging environment.
- Added hydration warning suppression to the RootLayout for improved rendering.
- Enhanced ConsoleStatusPage with localization support and improved health status display.
- Refactored event and course management UI components for better user experience and consistency.
- Updated translations for console status page in Arabic, English, and Spanish.

#### feat: update robots.txt and enhance console page components

- Added "/console" to the disallowed paths in robots.txt to prevent indexing.
- Refactored ConsolePage to improve UI components, including pagination and event display logic.
- Integrated new hooks for better state management and localization in ConsolePage.
- Updated event handling and metadata generation for improved user experience across console pages.

### 2026-03-28

#### feat: enhance date formatting and UI components across various pages

- Integrated `useDateFnsLocale` hook for consistent date formatting in ConsolePage, CertificatesContent, and BillingSettingsPage.
- Updated date display logic to use `date-fns` for improved localization and formatting.
- Refactored button and chip components for better styling and user experience in community and creator pages.
- Enhanced pagination and loading states in CoursesResults and CreatorActivityPage for improved performance and usability.
- Removed redundant date formatting functions to streamline code and improve maintainability.

#### feat: enhance email verification process and improve user feedback

- Updated VerifyEmailPage to handle OTP verification with improved state management and user feedback.
- Introduced new translations for OTP verification messages in multiple languages.
- Enhanced error handling for invalid or expired verification codes in the API routes.
- Added new API endpoints for checking contact email and phone availability, improving user experience during profile updates.
- Refactored global CSS to streamline styles for dropdown and select components.

#### feat: enhance form validation and error handling in authentication pages

- Added new error handling logic for the ForgotPasswordPage to provide more specific feedback based on API responses.
- Updated the LoginPage to improve error messaging and introduced new callback URLs for better navigation.
- Refactored the RegisterPage to include enhanced error mapping for registration failures and improved user feedback.
- Introduced new CSS styles for error states in forms to enhance user experience.
- Added RTL support for input groups and progress bars in the global CSS.

#### feat: enhance event and course editing experience with loading skeletons

- Integrated `CreatorSkeleton` component for loading states in EditCoursePage and EditEventPage, improving user experience during data fetching.
- Updated translations for event management to include new labels and descriptions in Arabic, English, and Spanish.
- Refactored EventsPage to streamline loading logic and improve overall layout consistency.

#### feat: enhance course and event management UI and seeding logic

- Updated CourseOverviewPage and EventOverviewPage to utilize new button variants and improved styling for better user experience.
- Refactored event and course seeding logic to include realistic enrollment and registration statuses, enhancing data integrity.
- Introduced utility functions for managing payment statuses and timestamps for event registrations and course enrollments.
- Improved overall layout and responsiveness of event and course detail pages.
- Adjusted seed configuration for courses and events to allow for more realistic capacities and fill ratios.

#### feat: enhance community post editor and improve translations

- Added required validation for title and description fields in the community post editor.
- Updated labels for clarity, changing "quickSummary" to "summary" and "postTitle" to "title".
- Improved styling for buttons and tabs in the CreatePostFAB component for better user experience.
- Updated translations in Arabic, English, and Spanish to reflect changes in field names and descriptions.

### 2026-03-27

#### refactor: update post structure and improve content handling

- Replaced `content` with `description` in various components to enhance clarity and consistency.
- Updated form validation to reflect changes in post body and description requirements.
- Adjusted seeding logic to generate appropriate content for posts.
- Modified translations to include new fields for post body and description.
- Improved styling and layout in community post editor and detail pages for better user experience.

#### feat: add gallery image support to posts

- Introduced a new `galleryImageUrls` field in the Post model to store multiple image URLs.
- Updated API routes to handle gallery images during post creation, retrieval, and updates.
- Enhanced PostDetailPage to display gallery images if available.
- Added translations for gallery image alt text in multiple languages.
- Updated seeding functionality to include fake gallery image URLs for testing.

#### refactor: update styling and enhance seeding functionality

- Updated card component styles in CourseOverviewPage and EventGeneralSection for improved visual consistency.
- Commented out unused class names in EditEventPage to clean up the code.
- Enhanced seeding functionality by adding a new utility function for generating fake gallery image URLs and integrating it into course and event seeders.
- Improved animation handling in EventDetailTabs by utilizing framer-motion for smoother transitions.

### 2026-03-26

#### chore: bump package versions to 1.1.4 for core and app

- Updated version in package.json for both @logi-x/experts and @logi-x/experts-app to 1.1.4 for consistency.

#### chore: update dependencies and improve event section component

- Bump various dependencies in package.json and pnpm-lock.yaml for better performance and security.
- Refactor EventsSection component to use updated HeroUI components and improve code readability.
- Update SQL seed file name in staging commands for consistency.

</details>

---

<details>
<summary><strong>[1.1.3] — 2026-03-20 - 2026-03-26</strong> — expand for full notes</summary>

<br />

[Google Docs V1.1.3](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?pli=1&tab=t.troonsh9pz1k)

### 2026-03-26

> [!NOTE]
> RELEASE CANDIDATE

#### docs(10-05): complete overlay components migration plan

- SUMMARY.md with 23 files migrated across Dialog/AlertDialog/Sheet/DropdownMenu
- STATE.md advanced to plan 6 of 6
- ROADMAP.md progress updated

#### feat(10-05): migrate DropdownMenu to HeroUI Dropdown compound components

- DropdownMenu → Dropdown with Dropdown.Trigger/Popover/Menu/Item/Section/Separator
- DropdownMenuTrigger asChild → Dropdown.Trigger wrapping child directly
- onSelect → onPress on Dropdown.Item
- DropdownMenuLabel → Dropdown.Section title or pointer-events-none item
- DropdownMenuGroup → Dropdown.Section
- 4 consumer files: Navbar, navbar-v2, nav-user, bookmarks

#### feat(10-05): migrate Dialog/AlertDialog/Sheet to HeroUI Modal/AlertDialog/Drawer

- Dialog → Modal with compound pattern (Modal.Backdrop/Container/Dialog/Header/Heading/Body/Footer)
- AlertDialog → HeroUI AlertDialog with trigger-based and controlled patterns
- Sheet → Drawer with placement prop (left for sidebars, bottom for mobile sheets)
- useOverlayState for controlled modal state management
- disabled → isDisabled on HeroUI Button props
- 19 consumer files migrated across courses, events, community, creator, affiliate

#### docs(10-04): complete form components migration plan

_(No body in commit.)_

#### feat(10-04): migrate shadcn Select to HeroUI Select+ListBox compound pattern in 19 consumer files

- Replace Select/SelectTrigger/SelectValue/SelectContent/SelectItem with HeroUI Select compound + ListBox
- Convert onValueChange to onChange, disabled to isDisabled
- Add Select.Trigger, Select.Value, Select.Indicator, Select.Popover + ListBox + ListBox.Item
- Fix Textarea->TextArea casing bug in event-general-section
- Add missing Input import to event-agenda-section

#### feat(10-04): migrate shadcn Input, Label, Textarea, Checkbox, RadioGroup to HeroUI equivalents

- Replace shadcn Input/Label imports with HeroUI equivalents in 18 files
- Migrate Checkbox: checked->isSelected, onCheckedChange->onChange
- Migrate RadioGroup: onValueChange->onChange, RadioGroupItem->Radio
- Migrate Textarea->TextArea (capital A) for HeroUI naming
- Fix missing HeroUI imports in lesson-dialog and quiz-dialog (Rule 1 bug fix)

### 2026-03-19

#### docs(10-03): complete Badge-to-Chip and Card compound migration plan

_(No body in commit.)_

#### feat(10-03): migrate shadcn Card to HeroUI Card compound components in 39 consumer files

- Replace all Card/CardHeader/CardTitle/CardDescription/CardContent/CardFooter imports
  from @/components/ui/card with Card from @heroui/react
- Convert to compound component pattern: CardHeader -> Card.Header, CardTitle -> Card.Title,
  CardDescription -> Card.Description, CardContent -> Card.Content, CardFooter -> Card.Footer
- Add Card to existing @heroui/react imports or create new imports as needed
- Fix missing Card import in activity-feed.tsx, timeline-activity-item.tsx
- Include event-pricing-section.tsx (discovered during migration, not in plan but uses shadcn Card)

#### feat(10-03): migrate shadcn Badge to HeroUI Chip in 43 consumer files

- Replace all Badge imports from @/components/ui/badge with Chip from @heroui/react
- Map variant="secondary" to variant="flat", variant="outline" to variant="bordered"
- Map variant="destructive" to color="danger", variant="default" to variant="solid"
- Preserve all className props and custom styling
- Fix duplicate Chip imports in Navbar and navbar-v2
- Replace Badge with Chip in commented code blocks for consistency

#### docs(10-02): complete Button migration plan - 68 files migrated to HeroUI

_(No body in commit.)_

#### fix(10-02): remove duplicate className prop in events calendar page

- Fixed duplicate className on Button caused by asChild migration

#### refactor: remove AppSidebar and NavUser components

- Delete AppSidebar and NavUser components from the experts-app, streamlining the codebase.
- This change eliminates unused sidebar and user navigation functionalities, improving overall application performance and maintainability.

#### feat(10-02): migrate shadcn Button imports to HeroUI in src/ component and library files

- Replace all `import { Button } from "@/components/ui/button"` with `import { Button } from "@heroui/react"` across 27 src/ files
- Merge Button into existing @heroui/react imports where applicable
- Convert variant="destructive" to color="danger"
- Convert disabled prop to isDisabled on Button elements
- Convert size="icon" to isIconOnly
- Convert asChild pattern to as={Link} with href prop
- src/components/ui/button.tsx left untouched

#### feat(10-02): migrate shadcn Button imports to HeroUI in app/ page files

- Replace all `import { Button } from "@/components/ui/button"` with `import { Button } from "@heroui/react"` across 41 app/ files
- Merge Button into existing @heroui/react imports where applicable
- Convert variant="destructive" to color="danger"
- Convert disabled prop to isDisabled
- Convert size="icon" to isIconOnly
- Convert asChild pattern to as={Link} with href prop

#### docs(10-01): complete color token standardization plan

- Add 10-01-SUMMARY.md documenting 484 violet/purple replacements across 83 files
- Update STATE.md with plan progress, metrics, and decisions
- Update ROADMAP.md with plan 01 completion status

#### feat(10-01): replace hardcoded violet/purple colors with primary tokens in src/ files

- Replace all violet/purple Tailwind classes with primary token equivalents across 31 src/ component and library files
- Remove redundant dark:text-violet-_, dark:bg-violet-_ overrides
- Add BRAND_PRIMARY_HEX constant in OG image files (CSS variables unavailable in OG context)
- Replace #2879dc hex values with BRAND_PRIMARY_HEX in og-presets.ts and generate-og-image.tsx
- No src/components/ui/ files were modified

#### feat(10-01): replace hardcoded violet/purple colors with primary tokens in app/ files

- Replace all text-violet-_, bg-violet-_, border-violet-_, ring-violet-_, from-violet-_, to-violet-_ with primary equivalents across 52 app/ page files
- Replace text-purple-_, bg-purple-_ with primary equivalents
- Remove redundant dark:text-violet-_, dark:bg-violet-_ overrides (CSS variable handles dark mode)
- Handle special cases: OG live page defaults, console categorical colors, about page gradient

#### fix(10): revise plans 10-05 and 10-06 based on checker feedback

_(No body in commit.)_

#### docs(10): create phase plan for shadcn-to-HeroUI migration and color token standardization

_(No body in commit.)_

#### docs(10): add phase 10 planning artifacts — roadmap, state, validation strategy

_(No body in commit.)_

#### docs(10): research phase domain - shadcn to HeroUI migration and color token standardization

_(No body in commit.)_

#### refactor: enhance chart rendering and loading states in analytics and dashboard components

- Introduce ChartMountGuard component to manage chart dimensions dynamically, improving rendering during animations.
- Update InstructorAnalyticsPage and CreatorDashboardPage to utilize ChartMountGuard for better chart responsiveness.
- Modify CreatorLayoutV2 and AppSidebarShell to support enhanced loading states with detailed loading messages.
- Refactor various components to improve maintainability and user experience, ensuring a smoother interaction flow.

#### chore: update dependencies and refactor components for improved performance

- Bump versions of several dependencies in package.json, including AWS SDK and Next.js packages, for enhanced functionality and compatibility.
- Refactor InstructorAnalyticsPage to utilize new CreatorLayoutV2 component and improve access control checks.
- Remove unused hooks and components, including use-mobile.ts and logo.tsx, to streamline the codebase.
- Update AppSidebarShell and related components to enhance sidebar functionality and improve loading states.
- Clean up and optimize various UI components for better maintainability and user experience.

### 2026-03-18

#### chore: update dependencies and enhance course management features

- Bump versions of several dependencies in package.json for improved functionality and compatibility, including AWS SDK and Heroui components.
- Refactor global CSS to support RTL layouts and improve styling for various components.
- Introduce new CoursesResults component for better course management, including pagination and filtering options.
- Update CreatorPage and related components to utilize new layout and styling conventions.
- Enhance AdminProcessingFeeCalculatorPage with internationalization support for better user experience.

### 2026-03-15

#### feat: add NotFound page and enhance profile form validation

- Introduce a new NotFound page component with internationalization support.
- Refactor CompleteProfilePage to utilize dynamic validation messages based on translations.
- Update form validation schema to improve user feedback and error handling.
- Clean up unused CSS files and streamline global styles for better maintainability.

</details>

---

[1.1.2]
<br />
.
<br />
.
<br />
.
<br />
[1.0.1]

---

<details>
<summary><strong>[1.0.0] — 2024-10-09</strong> — expand for full notes</summary>

## [1.0.0] — 2024-10-09

### Initial release (baseline)

- Full-stack Next.js monolith with CQRS-influenced domain layer
- PostgreSQL + Prisma ORM, NextAuth v5 authentication
- Creator console for courses and events management
- Multi-locale support (EN, AR, ES) via next-intl
- Stripe, Noon, and Tabby payment gateway integrations
- ZATCA compliance integration
- Community posts with Markdown editor
- Real-time diagnostics console with SSE streaming
- System health status page

</details>
