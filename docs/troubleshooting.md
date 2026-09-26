# Troubleshooting

## Python is not found

Install Python 3.10 or newer and open a new terminal. On Windows, if the Python
launcher is available, use `py -3 -m venv .venv` to create the environment. Then
use the explicit `.venv` executable paths from the README.

## `ModuleNotFoundError: No module named 'nicegui'`

Install requirements and launch using the same interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Using a globally installed Python to launch the app will not automatically use
packages installed in `.venv`.

## PowerShell blocks environment activation

Activation is optional. Run `.\.venv\Scripts\python.exe` directly as shown in
the README; no execution-policy change is needed.

## Port 8080 is already in use

Stop the previous app instance with `Ctrl+C` in its terminal, or change the final
`ui.run` call to use another port, for example `port=8081`. Open the corresponding
URL, http://localhost:8081.

## The browser cannot connect

Keep the terminal running and inspect it for startup errors. Use
http://127.0.0.1:8080 on the same computer that runs Python. The sample binds only
to localhost, so another computer cannot connect to it directly. Use HTTP, not HTTPS.

## A task is missing or the counts seem different

Clear the search and select All. Filters affect the visible list, while the
cards, chart, and CSV export use all tasks. Reloading discards edits and restores
the five sample tasks. Separate tabs each have independent data.

## Tests fail to find the application

Run tests from the repository root, where `pytest.ini` and `main.py` are located,
and install `requirements-dev.txt` into the same virtual environment. The provided
pytest configuration identifies the app entry point and enables async tests.

## Check installed dependencies

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip show nicegui
.\.venv\Scripts\python.exe -m pip check
```

When reporting an issue, include the command you ran, Python and NiceGUI versions,
the full error traceback, and steps to reproduce the problem.

[Back to README](../README.md)
