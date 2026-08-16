# Doctrin Todo v4.1.0 – Test Log

**Date:** 2026-08-16  
**Scope:** Pre-publication verification of Today fix, synced editable backlog, prompt generation, editable/collapsible paths, and full regression coverage.

## Summary

- JavaScript syntax (`node --check`): **PASS**
- HTML parse and unique IDs: **PASS**
- Static security/config assertions: **6/6 PASS**
- Latest local automated functional/regression suite after browser-found render fix: **63/63 PASS**
- Legacy v3 seed migration: **201/201 tasks imported**; nested paths preserved; backlog preserved
- Dropbox API behavior: revision-aware update and 409 handling tested with deterministic mocks
- Live Dropbox write was intentionally not performed during automated testing to avoid touching user production data.

## Root cause verified – Today bug

v4.0.0 excluded tasks from Today/Overdue when `Next wk` was also set. v4.1.0 makes the due date authoritative: a task dated today is shown in Today even if it is also tagged Next wk. The task remains eligible for the Next wk view because of the tag.

## Automated functional and regression tests

1. **PASS** — JS API version is 4.1.0
2. **PASS** — Data version is 5
3. **PASS** — Legacy task normalizes
4. **PASS** — Today includes due-today
5. **PASS** — REGRESSION Today includes due-today + Next wk
6. **PASS** — REGRESSION overdue includes Next wk tag
7. **PASS** — Today excludes tomorrow
8. **PASS** — Next wk includes tag without date
9. **PASS** — Next wk includes next-week date
10. **PASS** — Upcoming includes overdue
11. **PASS** — Follow-up filter
12. **PASS** — Sometimes filter
13. **PASS** — Markdown hierarchy
14. **PASS** — Path parse slash
15. **PASS** — Path parse chevron
16. **PASS** — Path parse greater-than
17. **PASS** — Path normalization updates level
18. **PASS** — Path group HTML has header and task
19. **PASS** — Path group collapse hides tasks
20. **PASS** — Collapsed path persists
21. **PASS** — Inline renderer includes path editor
22. **PASS** — New task path saved
23. **PASS** — Default backlog has 4 migrated improvements
24. **PASS** — Backlog bug type
25. **PASS** — Backlog comment preserved
26. **PASS** — Backlog selected flag preserved
27. **PASS** — Prompt includes selected bug and comment
28. **PASS** — Prompt excludes unselected
29. **PASS** — Prompt excludes done
30. **PASS** — Export payload includes backlog
31. **PASS** — Old JSON import preserves backlog
32. **PASS** — New JSON import restores backlog
33. **PASS** — Remote payload includes backlog
34. **PASS** — Snapshot contains todos and backlog
35. **PASS** — Rollback restores backlog
36. **PASS** — Undo restores tasks and backlog
37. **PASS** — Completion visible until clear
38. **PASS** — Clear hides from open
39. **PASS** — Log includes cleared complete
40. **PASS** — Search matches path
41. **PASS** — Weekly rollover promotes stale Next wk
42. **PASS** — Tag toggle Next wk
43. **PASS** — Tag toggle Follow-up
44. **PASS** — Tag toggle Sometimes
45. **PASS** — Dropbox update mode protects revision
46. **PASS** — Dropbox 409 download recognized as missing
47. **PASS** — Remote v4 missing backlog preserves local backlog
48. **PASS** — Remote v5 replaces backlog
49. **PASS** — Full 201-item v3 seed imports without loss
50. **PASS** — PKCE authorize URL has client id, redirect and S256 challenge
51. **PASS** — Dropbox upload conflict is surfaced
52. **PASS** — Backlog comment changes data hash
53. **PASS** — Improvement prompt label is correct
54. **PASS** — Collapse keys are scoped by view/context
55. **PASS** — Old snapshot without backlog preserves current backlog
56. **PASS** — Render Today count includes Next wk-tagged today task
57. **PASS** — Backlog open count excludes done items
58. **PASS** — Version history current is 4.1.0
59. **PASS** — History HTML includes synced backlog UI
60. **PASS** — Upcoming rendering prioritizes Today over Next flag

## Static and structural checks

- No duplicate HTML element IDs.
- Exactly one application script block.
- Dropbox App key retained; redirect URI retained.
- No Dropbox client/app secret embedded.
- No initial Doctrin todo content embedded in the public HTML.
- `backlog` included in local persisted schema, export payload, snapshot payload, and Dropbox remote payload.
- Today predicate contains no exclusion based on `Next wk`.

## Compatibility / migration

- Existing localStorage key is unchanged: `doctrin-things-todo-v1`.
- Existing Dropbox file remains `/todos.json`.
- v3/v4 JSON without a `backlog` field imports without erasing the current backlog.
- Existing Dropbox v4 data without a backlog is treated as a migration case: tasks are retained and backlog is added on the next safe save.
- Old snapshots that contain only tasks can still be restored without deleting the current backlog.

## Test environment

- Node: `v22.16.0`
- Browser available in container: `Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)`

## Browser test limitation

A real Chromium/CDP integration run was attempted. The managed container browser blocks both localhost and `file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. This is an environment policy, not an application failure. Because of that, no claim of local visual/browser execution is made in this log.

For publication, the recommended final gate is a temporary GitHub Actions browser smoke test against the candidate branch, followed by removal of temporary test workflow files before merge.

## Result

**Pre-publication local verification: PASS.** No failing functional, regression, migration, syntax, structure, or static security checks remain.


## Publication-gate defect found and corrected
A real Chromium gate found that the Today count was correct while the list rendering was empty. Date helpers accepted an optional test `base` argument but had been passed directly to `Array.filter`, so JavaScript supplied the array index as that date base. All affected callbacks are now explicit one-argument arrows. Regression tests cover Today rendering, overdue rendering and Upcoming/Next wk counters.

Latest local deterministic suite: **63/63 PASS**.

## GitHub Actions final browser gate
- Exact candidate hash/size: **PASS**
- JavaScript syntax: **PASS**
- Embedded suite in real Chromium: **54/54 PASS**
- Today due-date + Next wk rendering: **PASS**
- Upcoming and Next wk dated counters: **PASS**
- Same-path collapse/expand: **PASS**
- Path editing: **PASS**
- Editable backlog, implementation comment and prompt generation: **PASS**
- Add improvement backlog item: **PASS**
- Browser page errors in tested flows: **0**
- Live Dropbox write: not performed to protect production data; deterministic sync tests cover serialization/revision/conflict behavior.

**Final publication gate: PASS.**
