# Focus Desk — a NiceGUI sample

A small interactive task dashboard written in Python. Includes task creation,
completion and deletion, live search and status filtering, summary cards, an
ECharts progress chart, a dialog, notifications, and CSV export.

## Features

| Feature | Behavior |
| --- | --- |
| Task board | Starts with five example tasks across Design, Development, and Learning. |
| New task dialog | Accepts a trimmed, nonempty title up to 120 characters and a category. |
| Completion | Check or uncheck a task to update all summary cards and the chart. |
| Search and filters | Combine case-insensitive title search with All, Open, or Complete status. |
| Delete | Remove a task immediately using its close button. |
| Progress chart | Shows the percentage of all tasks completed. |
| CSV export | Downloads all tasks, including tasks hidden by filters. |
| Responsive layout | Stacks panels on smaller screens and uses columns on larger screens. |

## Documentation

- [User guide](docs/user-guide.md): walkthrough, filters, exports, and data lifetime.
- [Development guide](docs/development.md): project structure, state flow, customization, and testing.
- [Troubleshooting](docs/troubleshooting.md): installation and startup problems.

## Run locally

Requires Python 3.10 or newer.

Clone this repository and enter the project directory:

```sh
git clone https://github.com/mojammelhuque/NiceGUI.git
cd NiceGUI
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Open **http://localhost:8080**. Stop the server with `Ctrl+C`.

On macOS/Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

If port 8080 is occupied, change `port` in the `ui.run(...)` call.

Dependencies are installed in `.venv`; activating that environment is optional
because these commands invoke its Python executable directly. The runtime
dependency is pinned to NiceGUI 3.17.1. This sample was verified on Python 3.13.

## Explore the code

Everything is in `main.py` to make the example easy to follow:

- `Task` holds each task's data.
- `dashboard()` builds the page and owns its independent state.
- Event handlers update tasks, validate input, and export CSV.
- `@ui.refreshable` functions rebuild the cards, task list, and chart.
- Tailwind classes and a little CSS provide a responsive layout.

Data is in memory per page: reloading restores the sample tasks. There is no
database or authentication. The server binds to localhost for local development.
To extend the example, try adding due dates or persisting tasks in SQLite.

Reference: [NiceGUI documentation](https://nicegui.io/documentation).

## Verify

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use NiceGUI's simulated user to exercise page loading, input validation,
task creation, search, completion, deletion, CSV export, and reset on reload.

## RStudio Community Edition POC

See [the walkthrough](docs/rstudio-poc.md) to open NiceGUI.Rproj and run the ASGI app from RStudio's Terminal.
