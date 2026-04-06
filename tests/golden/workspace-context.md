# PersonalOS Workspace Context

Use this file as public-safe assistant context for the starter workspace.

## Workspace Summary

- Projects: 3
- Tasks: 5
- Decisions: 3

## Active Projects

### Local Habit Tracker

- ID: `prj_local_habit_tracker`
- Status: `active`
- Summary: Build a private-first habit tracker with a calm daily check-in and exportable weekly review notes.
- Tags: product, ios, habits
- Body: This sample project demonstrates a healthy middle stage: the concept is clear, the core loop is defined, and a few important product decisions are still in motion.

### Starter Workspace Launch

- ID: `prj_starter_workspace`
- Status: `deploy_ready`
- Summary: Ship a cloneable PersonalOS starter with sample data, a validation CLI, and deterministic generated outputs.
- Tags: docs, tooling, starter
- Body: This meta project keeps the public template honest by focusing on onboarding quality, deterministic tooling, and public-safe sample content instead of private operating detail.

### Portfolio Site Refresh

- ID: `prj_portfolio_refresh`
- Status: `building`
- Summary: Refresh the public portfolio so it explains services, proof of work, and writing more clearly.
- Tags: portfolio, design, writing
- Body: The project is tightening positioning, simplifying navigation, and packaging a cleaner proof-of-work story for future clients and collaborators.

## Open Tasks

- `tsk_habit_checkin_flow` Define the v1 habit check-in flow [ready]
  - Project ID: `prj_local_habit_tracker`
  - Summary: Map the daily flow so the habit tracker feels quick, private, and calm from the first session.
- `tsk_offline_sync_options` Compare offline sync options [blocked]
  - Project ID: `prj_local_habit_tracker`
  - Summary: Compare local-only storage against optional backup sync so the app stays private without boxing in future needs.
- `tsk_case_study_screenshots` Capture case study screenshots [ready]
  - Project ID: `prj_portfolio_refresh`
  - Summary: Export before and after screenshots so the portfolio refresh has immediate visual proof.
- `tsk_homepage_positioning` Draft homepage positioning copy [in_progress]
  - Project ID: `prj_portfolio_refresh`
  - Summary: Write a sharper hero section and service overview for the refreshed portfolio homepage.

## Decision Notes

- `dec_static_first_portfolio` Choose a static-first portfolio stack [decided]
  - Outcome: commit
  - Summary: Keep the portfolio refresh simple by using a static-first deployment with lightweight analytics and no custom backend.
- `dec_private_first_habits` Keep the habit tracker private-first [proposed]
  - Outcome: revisit
  - Summary: Start with local-only storage and revisit optional sync only after the daily habit loop feels dependable.
- `dec_vertical_slice_first` Ship a vertical slice before broader coverage [decided]
  - Outcome: commit
  - Summary: Prove the starter with projects, tasks, and decisions before expanding into tools, contacts, applications, and reviews.
