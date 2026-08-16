# Doctrin Todo v4.2.0 – Test Log

**Date:** 2026-08-16

## Scope
Synced development jobs, safe agent-handoff preparation, local friction monitoring, friction-to-backlog bug creation, v5→v6 migration, v6 import/export parity, and regression of existing functionality.

## Architecture and privacy
- Development jobs are stored with todos/backlog in Dropbox `/todos.json`.
- Raw friction telemetry is local-only in `doctrin-todo-friction-v1`; it is excluded from Dropbox/export/remote payloads.
- Telemetry stores technical action/target IDs, timestamps and small result metadata, not todo text or raw search strings.
- Turning a friction signal into a bug creates a normal synced backlog item.
- No OpenAI API key, GitHub PAT or other development credential is embedded in the public client.
- Agent handoff is copy-only; the public app never publishes backlog content to GitHub. Full unattended execution requires a separate authenticated bridge.

## Friction rules tested
- Repeated no-op click: >=3 same target / 20 s.
- Undo burst: >=3 / 2 min.
- Toggle loop: >=4 same object / 3 min.
- Edit churn: >=4 same todo / 5 min.
- Navigation bounce: >=6 changes among <=3 views / 2 min.
- Repeated zero-result search: >=3 same hashed query / 90 s.
- Sync trouble: >=2 errors / 10 min.
- Rollback loop: >=2 / 10 min.
- Ten-minute per-signal cooldown/deduplication.

## Final automated gate
- JavaScript syntax: **PASS**
- HTML IDs / structural assertions: **PASS**
- Credential/private-data/public-issue static scan: **PASS**
- `git diff --check`: **PASS**
- Real Chromium embedded regression suite: **74/74 PASS**
- Real Chromium v5→v6 normal UI migration: **PASS**
- Today + Next wk regression: **PASS**
- Selected backlog → development job → persisted prompt: **PASS**
- Safe agent-handoff UI: **PASS**
- Friction signal detection/rendering: **PASS**
- Friction signal → synced backlog bug: **PASS**
- Friction telemetry excluded from remote payload: **PASS**
- v6 export/import development-job roundtrip: **PASS**
- Browser page errors in tested flows: **0**

## Existing regression coverage
The embedded suite retains coverage for Today/Upcoming/Next wk, Follow-up/Sometimes, hierarchy/path editing, collapse/expand, import/export, completion/log, keyboard controls, undo/snapshots/rollback, Dropbox revision conflicts and earlier-schema migration.

**Publication candidate gate: PASS.**
