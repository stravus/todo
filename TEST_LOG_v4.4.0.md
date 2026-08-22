# Todo v4.4.0 – Test Log

**Date:** 2026-08-22

## Scope
Seven workflow improvements: safer sync conflicts, a 14-day weekly schedule, todo comments with image attachments, stable completion order, drag-and-drop ordering/scheduling/categories, global clear-completed behavior, and an explicit Inbox.

## Compatibility and data
- Dropbox remains `/todos.json` and OAuth/storage keys are unchanged.
- Base data schema remains version 6; v4.4 adds additive `featureVersion: 1` metadata.
- Legacy schema-6 / feature-0 data is migrated in place to feature 1.
- Tasks gain optional `inbox`, `order`, `updatedAt`, and `comments[]` fields; legacy tasks receive safe defaults.
- Comment images are stored as image data URLs inside the todo JSON and therefore sync through the existing Dropbox file. UI limits selection to four images per comment and 2.5 MB per image.
- Tool-version restore blocks older feature-0 app versions once feature-1 data exists, preventing an older core from silently stripping v4.4 fields.
- No private todo data is stored in the repository or test fixtures.

## Behavior covered
- Conflict merge keeps unique records from both local and Dropbox copies and resolves same-ID collisions using the latest `updatedAt`/completion/creation timestamp. Local-only and Dropbox-only overrides remain available.
- Week view renders Monday–Sunday for the current and next week and supports drag scheduling.
- Inbox is explicit and accepts quick-add and drag-to-Inbox.
- Completed todos preserve their manual order until globally cleared.
- Drag-and-drop supports reordering, moving to a calendar day, moving to a path group, and moving to supported sidebar categories.
- Todo comments sync as task data and may contain text plus image attachments.
- “Rensa avklarade” clears every completed, uncleared todo regardless of the active view.

## Automated gate
Pending on the review branch. The gate runs syntax/static/privacy checks, the unchanged embedded core regression suite, legacy feature migration, Inbox, stable completion order, global clear, 14-day week rendering, real browser drag-and-drop, image-comment persistence, conflict merge logic, old-version compatibility blocking, desktop/mobile rendering and page-error checks.
