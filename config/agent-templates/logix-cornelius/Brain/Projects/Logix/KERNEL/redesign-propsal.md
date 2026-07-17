---
title: "redesign propsal"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Logix/KERNEL/redesign-propsal.md"
---
**Verdict**  
You can safely redesign the data model to a clean “company‑client” structure by consolidating the existing tenant‑related tables, tightening foreign‑key constraints, and adding a few strategic indexes and RLS policies. The changes are non‑destructive (expand → backfill → contract) and can be deployed with a short downtime window if you keep the migration scripts in separate steps.

---

## 1️⃣ Core “Bone” of the Data Model

| Table | Purpose | Key Columns | Relationships |
|-------|---------|-------------|---------------|
| **Account** (aka *Company*) | Top‑level tenant. Holds company metadata and a flag for the internal Logix account. | `id`, `name`, `slug`, `type`, `is_internal_singleton` | 1 ↔ N to all tenant‑specific tables |
| **Client** | A customer of an Account. | `id`, `account_id`, `name`, `slug`, `status`, `tags`, … | Many Clients per Account; optional FK to Project |
| **Project** | Work being done for a Client or directly for the Company. | `id`, `account_id`, `client_id?`, `producer_department_id?`, `kind`, `name`, `slug`, `code`, `status` | 1 ↔ N to Client (optional), Department, and many child tables |
| **User** | Authenticated users. | `id`, `email`, `name`, `password_hash`, `is_internal`, … | Many‑to‑many with Account via **AccountUser** |
| **AccountUser** | Role‑based membership of a User in an Account (and optionally a Client). | `account_id`, `user_id`, `client_id?`, `role` | FK to Account, User, optional Client |
| **Department** | Logical grouping of Users inside an Account. | `id`, `name`, `slug` | 1 ↔ N to User and Project |
| **Proposal / Invoice / Payment / Expense / Subscription / RevenueRecord / WorkLog** | Domain entities that belong to a particular Account, Client, or Project. All contain `account_id`. | `account_id`, `client_id?`, `project_id?`, … | Each FK references the owning tables |

> **Key point:** every tenant‑specific table now has an explicit `account_id` column and all relationships are enforced at the database level.

---

## 2️⃣ Multi‑Tenant Isolation

| Technique | Why it matters | Implementation |
|-----------|----------------|----------------|
| **Row‑Level Security (RLS)** | Prevents cross‑tenant data leakage even if the application code forgets to filter. | ```sql\nALTER TABLE project ENABLE ROW LEVEL SECURITY;\nCREATE POLICY tenant_isolation ON project USING (account_id = current_setting('app.account_id')::uuid);\n``` |
| **`current_setting('app.account_id')`** | Passes the authenticated Account ID into every query automatically via a PostgreSQL role or session variable. | In your Prisma client, set `setAppContext({ accountId: '...' })` before each request. |
| **Unique per‑tenant indexes** | Guarantees uniqueness of slugs, codes, etc., only within an Account. | ```prisma\n@@unique([account_id, slug])\n``` |

> **Tip:** If you need cross‑tenant reporting (e.g., admin dashboards), use a separate “admin” role that bypasses RLS or query with `SET LOCAL app.account_id = NULL`.

---

## 3️⃣ Soft Delete & Auditing

| Table | Strategy |
|-------|----------|
| All core tables | Add nullable `deleted_at` TIMESTAMP. Use partial unique indexes to treat deleted rows as invisible for uniqueness constraints: ```prisma\n@@unique([id, deleted_at])\n``` |
| Ledger‑related tables (`Invoice`, `Payment`, `Expense`) | **Immutable** – never UPDATE after INSERT. Instead create an audit table (e.g., `invoice_audit`). Trigger or application logic copies the old row to the audit table on UPDATE/DELETE. |
| `User` | Soft delete is optional; if used, add a `deleted_at` and enforce `WHERE deleted_at IS NULL`. |

---

## 4️⃣ Indexing Strategy

1. **Foreign‑Key indexes** – most tables already have them via Prisma (`@@index([account_id])`, etc.).
2. **Composite indexes for hot reads**  
   *Invoices* → `CREATE INDEX idx_invoice_client_status ON invoice(client_id, status);`  
   *Expenses* → `CREATE INDEX idx_expense_account_type_freq ON expense(account_id, type, frequency);`
3. **Partial unique indexes** – e.g., only enforce uniqueness on active rows:  
   ```sql
   CREATE UNIQUE INDEX uq_client_slug_active
       ON client (account_id, slug)
       WHERE deleted_at IS NULL;
   ```
4. **Covering indexes** for queries that read a handful of columns:  
   *Client list* → `CREATE INDEX idx_client_name_created ON client(account_id, name) INCLUDE (status, tags);`
5. **GIN index on JSONB columns** – e.g., `tags` if you query by tag value:  
   ```sql
   CREATE INDEX gin_client_tags ON client USING GIN(tags);
   ```

> **Rule of thumb:** For every SELECT that is executed > 1 % of the time, ensure there’s an index covering the WHERE columns and any ORDER BY fields.

---

## 5️⃣ Ledger & Money Handling

| Field | Type | Rationale |
|-------|------|------------|
| `amount`, `subtotal`, etc. | `NUMERIC(12,2)` (`@db.Decimal(12,2)`) | Avoid floating‑point; precise decimal arithmetic. |
| Currency code | `VARCHAR(3)` | ISO 4217, default to the company’s primary currency. |
| Double‑entry ledger | Two tables: `ledger_entry` (debit/credit pairs) and `ledger_balance`. | Each transaction is a single row per side; balances are derived via incremental materialized view or trigger. |

> **Never** store money in a floating type (`REAL`, `DOUBLE`). Use integer minor units (cents) if you need very fast arithmetic, but the Prisma schema already uses `Decimal`.

---

## 6️⃣ Vector / JSON Columns

*Vector* – The schema currently has `vector` extension enabled.  
- Ensure the dimension matches your embeddings (e.g., 1536 for OpenAI).  
- Use `ivfflat` index with an appropriate `nlist`.  
- Query with `@>`, `cosine_distance()`, etc.

*JSONB* – Used mainly for dynamic fields (`tags`, `config`, `rawData`).  
- Add GIN indexes only on columns that are queried by key/value.  
- Keep the size of JSONB payloads bounded; if they grow large, consider normalising into separate tables.

---

## 7️⃣ Migration Plan (Example: Adding a New `client_manager_id` to Client)

1. **Expand** – Add nullable column.  
   ```sql
   ALTER TABLE client ADD COLUMN client_manager_id UUID;
   ```
2. **Backfill** – Populate with default or derived values if needed; otherwise leave NULL.  
3. **Contract** – Add NOT NULL constraint (after ensuring no NULLs) and a foreign key to User.  
   ```sql
   ALTER TABLE client ALTER COLUMN client_manager_id SET NOT NULL;
   ALTER TABLE client ADD CONSTRAINT fk_client_manager FOREIGN KEY (client_manager_id) REFERENCES user(id);
   ```

> **Rollback** – Drop the column: `ALTER TABLE client DROP COLUMN IF EXISTS client_manager_id;`.

---

## 8️⃣ Operational Notes

| Aspect | Consideration |
|--------|---------------|
| **Locks** | Use `SELECT … FOR UPDATE` on ledger rows. Avoid table‑level locks when possible. |
| **Transaction size** | Keep business logic transactions < 1 s to avoid blocking writes. |
| **Batching** | For bulk inserts (e.g., WorkLog batches), use `INSERT ... ON CONFLICT DO NOTHING` and bulk commit every 10k rows. |
| **Monitoring** | Watch query plans (`EXPLAIN ANALYZE`) for the top 5 queries; check index hit rates. |
| **Backups** | Ensure PITR (Point‑in‑Time Recovery) is enabled; schedule nightly WAL archiving. |

---

## 9️⃣ Open Questions

1. **Row counts & traffic patterns** – How many rows per table will you reach in the next year?  
2. **Cross‑tenant reporting** – Will there be dashboards that aggregate data across all accounts?  
3. **Vector usage** – What embeddings dimension do you plan to store, and how many rows will they have?  
4. **Audit requirements** – Are there regulatory rules (e.g., GDPR) that require immutable audit logs for invoices or payments?

Answering these will let us fine‑tune partitioning strategies, decide on materialized views vs. real‑time aggregates, and choose the right index types.

---

### Bottom line

- Keep **Account** as the single source of truth for tenancy.
- Add `account_id` to every tenant‑specific table; enforce with FK + RLS.
- Use **soft delete** with partial unique indexes and a dedicated audit trail for ledger tables.
- Tailor indexes to your most frequent queries, adding composite or covering indexes where needed.
- Follow the expand → backfill → contract migration pattern to keep deployments zero‑downtime.

Feel free to let me know which specific part you’d like to dive deeper into (e.g., a particular table redesign, index tuning, or migration scripts).