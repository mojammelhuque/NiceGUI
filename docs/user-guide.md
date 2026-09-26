# User guide

## Start the dashboard

Follow the [installation steps](../README.md#run-locally), start `main.py`, and
open http://localhost:8080. The app does not open a browser automatically.

The initial board contains five tasks, with two already complete. The three
summary cards show total, in-progress, and completed tasks. The momentum chart
starts at 40%.

## Add and manage tasks

1. Click **New task**.
2. Enter a task name and choose Design, Development, or Learning.
3. Click **Add task**, or press Enter while the task-name field is focused.
4. Check a task to mark it complete; uncheck it to reopen it.
5. Click the close icon at the end of a task row to delete it immediately.

Task names are trimmed. Empty or whitespace-only names are rejected, and the
maximum length is 120 characters. Duplicate names are allowed. New tasks default
to the Development category. Cancel closes the dialog without adding a task;
the current draft remains in the fields until changed or the page reloads.

There is no undo for deletion. Reloading restores the entire initial demo dataset
and discards all changes, rather than restoring only the deleted task.

## Search and filter

Search matches any part of a task's title without regard to letter case. It does
not search category names. Use the status selector to show **All**, **Open**, or
**Complete** tasks. Search and status apply together.

The count below the board shows matching tasks out of the total. Summary cards
and the progress chart always describe the entire board, regardless of filters.
If a task disappears after you change its completion status, check the active
status filter. Clear the search and select All to see everything again.

## Export CSV

Click **Export CSV** to download `focus-desk-tasks.csv` with these columns:

| Column | Contents |
| --- | --- |
| Task | Task title |
| Category | Design, Development, or Learning |
| Status | Open or Complete |

The export includes every task in creation order, even when a filter is active.
It uses UTF-8 with a byte-order mark for spreadsheet compatibility. Formula-like
titles beginning with `=`, `+`, `-`, or `@` after leading whitespace receive a
leading apostrophe in the export. Commas and quotes are escaped by Python's CSV
writer. An empty board exports only the column headers.

CSV export is a snapshot; there is no CSV import feature.

## Data lifetime

Each page load creates its own in-memory task list. Separate tabs or visitors
do not share a board. Reloading the page or restarting the server restores the
example tasks. There are no accounts, database, or saved user preferences.

Use this as a local learning project. Persistence and authentication would need
to be added before adapting it into a shared task application.

[Back to README](../README.md)
