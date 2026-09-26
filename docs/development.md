# Development guide

## Project structure

```text
NiceGUI/
|-- main.py                 # Data model, page, handlers, and server entry point
|-- requirements.txt        # Pinned NiceGUI runtime dependency
|-- requirements-dev.txt    # Runtime plus test dependencies
|-- pytest.ini              # Async testing and application entry-point settings
|-- tests/
|   |-- conftest.py          # NiceGUI simulated-user pytest plugin
|   `-- test_dashboard.py    # Task workflow and reload checks
|-- docs/                   # User, development, and troubleshooting guides
`-- README.md               # Overview and quick start
```

The virtual environment, Python caches, test caches, NiceGUI storage directory,
environment files, and server logs are excluded by `.gitignore`.

## Page and state flow

`Task` is a dataclass with `title`, `category`, and `done` fields. The `/` route
is registered with `@ui.page('/')`. Each invocation of `dashboard()` creates a
fresh list of sample tasks and callbacks that close over that list.

The page defines three local `@ui.refreshable` views:

| View | Responsibility |
| --- | --- |
| `summary()` | Counts all tasks and renders three metric cards. |
| `task_list()` | Applies search and status, then renders task rows. |
| `breakdown()` | Computes completion percentage and builds the ECharts donut. |

Task creation, deletion, or a completion change mutates the page's list and calls
`refresh()`, which refreshes all three views. Search and status changes refresh
only `task_list()`. The form and filter controls sit outside those refreshable
regions, so a task update preserves their values.

Callbacks inside the task loop capture each task using a default argument, such
as `lambda e, t=task: set_done(t, e.value)`. This prevents every callback from
accidentally referring to the final task in the loop.

The chart uses rounded completion percentage and explicitly handles an empty
list to avoid division by zero. CSV is built in memory using `csv.writer` and
sent through `ui.download`; no export file is written on the server.

## Layout and styling

The interface uses NiceGUI components, Tailwind utility classes, and a short
`ui.add_css` block. `ui.colors` defines the primary and secondary accent colors.
The main area uses a three-column grid on large screens; the task board spans
two columns and the chart occupies one. Smaller screens stack the panels.

## Common customizations

- **Initial tasks:** edit the `tasks` list near the start of `dashboard()`.
- **Categories:** edit the `ui.select` options in the task dialog and any sample
  tasks that should use the new categories.
- **Colors:** change `ui.colors`, related CSS, and the chart's explicit colors.
- **Port:** change `port=8080` in the final `ui.run` call.
- **Development reload:** change `reload=False` to `reload=True` to restart on
  source changes. A restart resets the demo data.
- **Browser launch:** set `show=True` if you want startup to open a browser.

The `if __name__ == '__main__'` guard starts the local server when the file is
executed directly. It binds to `127.0.0.1`. Network hosting is outside this sample's
scope; a shared deployment also needs an appropriate persistence and access model.

## Testing

From the project root on Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

On macOS/Linux, substitute `.venv/bin/python` for the executable path.

The tests use NiceGUI's simulated-user plugin, so no browser driver or separately
running server is needed. They exercise initial rendering, empty-title validation,
task creation, search, completion, deletion, exported CSV content, and reload reset.
They do not verify browser appearance, responsive layout, or actual browser download
behavior. For visual review, open the running app at desktop and narrow widths,
try the status selector, and check the empty state after removing all tasks.

## Extension ideas

For a larger application, split data access from page rendering. Add stable task
IDs before introducing database updates or multiple-user editing. Persistence
could use SQLite for a local tool; shared boards also need explicit ownership and
concurrency decisions. Due dates, priority filters, and CSV import are separate
features that can build on the existing handlers and refreshable views.

## References

- [NiceGUI documentation](https://nicegui.io/documentation)
- [Refreshable UI](https://nicegui.io/documentation/refreshable)
- [ECharts component](https://nicegui.io/documentation/echart)
- [Server configuration](https://nicegui.io/documentation/run)

[Back to README](../README.md)
