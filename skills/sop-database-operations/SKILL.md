---
name: sop-database-operations
description: Beginner-safe guide to working with the company's databases — add, update, and query records safely. Use whenever touching SQLite/Postgres/MySQL data by hand.
---

# SOP — Database Operations (beginner-friendly)

**KPI:** 0 accidental data loss · every change verified + logged.

## The mental model
A database is a smart spreadsheet — it never corrupts, scales to millions of rows, and tracks every change.

## Safe workflow
1. **Read first** — `SELECT` to see what's there before changing anything.
2. **Back up** — snapshot before any `UPDATE`/`DELETE`.
3. **Use WHERE** — never run `UPDATE`/`DELETE` without a `WHERE` clause.
4. **Parameterize** — bind values, never string-concatenate (prevents SQL injection).
5. **Verify + log** — confirm the change and record what you did.

## Golden rules
- No `DELETE` without a backup.
- Always test on a copy first for anything destructive.
- When in doubt, `SELECT` before you `UPDATE`.
