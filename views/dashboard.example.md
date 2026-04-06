# PersonalOS Starter Dashboard

This dashboard is generated from the canonical markdown records in `entities/`.

## Snapshot

- Projects: 3 total (1 active, 1 building, 1 deploy_ready)
- Tasks: 5 total (1 blocked, 1 done, 1 in_progress, 2 ready)
- Decisions: 3 total (2 decided, 1 proposed)

## Projects

### Local Habit Tracker

- Status: `active`
- Priority: `medium`
- Summary: Build a private-first habit tracker with a calm daily check-in and exportable weekly review notes.
- Tags: product, ios, habits
- Open tasks: 2
- Decisions: 1 recorded
- Next tasks:
  - [ready] Define the v1 habit check-in flow (due 2026-04-10)
  - [blocked] Compare offline sync options (due 2026-04-12)
- Latest decision: Keep the habit tracker private-first (proposed)

This sample project demonstrates a healthy middle stage: the concept is clear, the core loop is defined, and a few important product decisions are still in motion.

### Starter Workspace Launch

- Status: `deploy_ready`
- Priority: `high`
- Summary: Ship a cloneable PersonalOS starter with sample data, a validation CLI, and deterministic generated outputs.
- Tags: docs, tooling, starter
- Open tasks: 0
- Decisions: 1 recorded
- Latest decision: Ship a vertical slice before broader coverage (decided)

This meta project keeps the public template honest by focusing on onboarding quality, deterministic tooling, and public-safe sample content instead of private operating detail.

### Portfolio Site Refresh

- Status: `building`
- Priority: `high`
- Summary: Refresh the public portfolio so it explains services, proof of work, and writing more clearly.
- Tags: portfolio, design, writing
- Open tasks: 2
- Decisions: 1 recorded
- Next tasks:
  - [ready] Capture case study screenshots (due 2026-04-09)
  - [in_progress] Draft homepage positioning copy (due 2026-04-08)
- Latest decision: Choose a static-first portfolio stack (decided)

The project is tightening positioning, simplifying navigation, and packaging a cleaner proof-of-work story for future clients and collaborators.

## Tasks To Move This Week

- [ready] Define the v1 habit check-in flow (Local Habit Tracker, due 2026-04-10)
  - Map the daily flow so the habit tracker feels quick, private, and calm from the first session.
- [blocked] Compare offline sync options (Local Habit Tracker, due 2026-04-12)
  - Compare local-only storage against optional backup sync so the app stays private without boxing in future needs.
- [ready] Capture case study screenshots (Portfolio Site Refresh, due 2026-04-09)
  - Export before and after screenshots so the portfolio refresh has immediate visual proof.
- [in_progress] Draft homepage positioning copy (Portfolio Site Refresh, due 2026-04-08)
  - Write a sharper hero section and service overview for the refreshed portfolio homepage.

## Completed Recently

- Publish quickstart and golden tests (Starter Workspace Launch)
  - Add a five-minute quickstart and deterministic tests so new builders can trust the sample workspace.

## Decision Log

- [decided] Choose a static-first portfolio stack (Portfolio Site Refresh, 2026-04-02)
  - Outcome: commit
  - Related task IDs: tsk_homepage_positioning, tsk_case_study_screenshots
  - Keep the portfolio refresh simple by using a static-first deployment with lightweight analytics and no custom backend.
- [proposed] Keep the habit tracker private-first (Local Habit Tracker, 2026-04-04)
  - Outcome: revisit
  - Related task IDs: tsk_habit_checkin_flow, tsk_offline_sync_options
  - Start with local-only storage and revisit optional sync only after the daily habit loop feels dependable.
- [decided] Ship a vertical slice before broader coverage (Starter Workspace Launch, 2026-04-05)
  - Outcome: commit
  - Related task IDs: tsk_quickstart_and_golden_tests
  - Prove the starter with projects, tasks, and decisions before expanding into tools, contacts, applications, and reviews.
