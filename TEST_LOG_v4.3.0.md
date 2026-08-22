# Todo v4.3.0 – Test Log

**Date:** 2026-08-22

## Scope
Tool-version snapshots/restore: switch the application code to a compatible earlier version without rolling back todos, backlog or development-job data.

## Architecture and compatibility
- v4.3.0 introduces a small same-origin version shell at the root URL.
- Exact application cores are immutable code-only files under `app-versions/`; no private todo data is stored there.
- v4.2.1 is preserved byte-for-byte as Git blob `2668975790e87a13d004b50c34c473db5d3062ce`.
- v4.2.0 is preserved byte-for-byte as Git blob `ab5484362d86ffdb4b7fc4cd246fb37c86aca48c`.
- v4.3.0 itself is archived as `app-versions/v4.3.0.html` for future restore support.
- The selected tool version is stored only in localStorage key `todo-app-version-pin-v1`; it is not part of Dropbox or exported todo data.
- Existing todo storage key `doctrin-things-todo-v1`, Dropbox `/todos.json`, OAuth settings and data schema are unchanged.
- Historical write-capable restore is allowed only when the stored data schema exactly matches the historical version (currently schema 6).
- Current v4.3.0 may read schema 5 specifically to let the unchanged v4.2.1 core perform its existing v5→v6 migration. Future/unknown schemas are blocked before an older core is loaded.
- Loading an older compatible core may change non-user metadata such as `appVersion`; tests require todos, backlog and development jobs to remain semantically identical.

## Local pre-PR quality gate
- Root bootstrap JavaScript syntax (`node --check`): **PASS**
- Generated injected version-manager JavaScript syntax: **PASS**
- Pure version-selection / compatibility / no-data-mutation tests: **PASS**
- Real Chromium shell/UI regression with synthetic generic data: **PASS**
- v5 shell pass-through without mutation: **PASS**
- future schema 7 block without mutation: **PASS**
- mobile 390 px version manager: **PASS**
- Browser page errors in local shell tests: **0**

## PR Chromium gate
GitHub Actions run `32559045490`: **PASS**.
- Static, syntax, snapshot and privacy checks: **PASS**
- Pure version-selection tests: **PASS**
- Real Chromium functional, migration and restore regression: **PASS**
- Unchanged v4.2.1 embedded regression suite: **PASS**
- Fresh v5→v6 migration: **PASS**
- Actual v4.3→v4.2.0→v4.3 and v4.3→v4.2.1→v4.3 switching: **PASS**
- Semantic preservation of todos, backlog and development jobs: **PASS**
- Future schema block without data mutation: **PASS**
- Mobile version-manager rendering: **PASS**
- Browser page errors in tested flows: **0**

The temporary PR-only test workflow was removed after the successful run and is not part of the release.

**Publication candidate gate: PASS.**
