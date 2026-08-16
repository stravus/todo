# Todo v4.2.1 – Test Log

**Date:** 2026-08-16

## Scope
Neutral visible branding: remove the Doctrin product name, add a compact checkmark logo, and keep existing todo/Dropbox data compatible.

## Compatibility decisions
- `DATA_VERSION` remains 6.
- Existing `doctrin-*` localStorage keys are intentionally retained so current browser data is not orphaned.
- Dropbox file path remains `/todos.json` and the existing OAuth configuration is unchanged.
- The user-visible/export payload app label changes from `Doctrin Todo` to `Todo`; task/backlog/development-job structures are unchanged.
- No private todo data is included in repository test fixtures; fixtures are generic synthetic records only.

## Automated quality gate
- Exact patch preconditions/assertions: **PASS**
- JavaScript syntax (`node --check`): **PASS**
- HTML ID uniqueness / structure: **PASS**
- Private-data / credential static scan: **PASS**
- `git diff --check`: **PASS**
- Real Chromium embedded functional/regression suite: **PASS (>=74 tests, all passing)**
- Real Chromium v5→v6 migration: **PASS**
- Todo preservation during migration: **PASS**
- Backlog preservation during migration: **PASS**
- Dropbox payload structure/version compatibility: **PASS**
- Neutral browser title + visible brand: **PASS**
- New logo visible on desktop: **PASS**
- New logo visible at 390 px mobile viewport: **PASS**
- Legacy `Doctrin` name absent from visible UI: **PASS**
- Browser page errors in tested desktop/mobile flows: **0**

## Existing regression coverage retained
The embedded suite continues to cover Today/Upcoming/Next wk, Follow-up/Sometimes, hierarchy/path editing, collapse/expand, import/export, completion/log, keyboard controls, undo/snapshots/rollback, Dropbox revision behavior, backlog/development jobs, friction monitoring and earlier-schema migration.

**Publication candidate gate: PASS.**
