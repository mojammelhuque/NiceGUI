# RStudio Community Edition proof of concept

This POC uses your personal GitHub repo and RStudio Desktop Community Edition.
RStudio is the editor and terminal; Python runs the backend on your computer.
It needs no office Connect access. This is a local preview, not cloud hosting.

## Open the project

Install RStudio Desktop with R, Python 3.10 or newer, and Git if needed.
Open `NiceGUI.Rproj` from your existing project folder in RStudio.
For a fresh clone, select **File > New Project > Version Control > Git** and use:

```text
https://github.com/mojammelhuque/NiceGUI.git
```

## Run from RStudio

Select the **Terminal** tab, not the R Console. From the project directory,
run these commands in a Windows PowerShell or Command Prompt terminal:

```text
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn connect_app:app --host 127.0.0.1 --port 8081
```

Skip environment creation if `.venv` already exists. If `python` is not found,
try `py -3 -m venv .venv`. If the terminal uses Git Bash, select PowerShell or
Command Prompt instead, or use forward slashes in the executable path.
On macOS/Linux use `python3` to create the environment and `.venv/bin/python`
for the subsequent commands.

Open **http://127.0.0.1:8081** in your browser. Keep the terminal running.
Port 8081 avoids conflicting with the original demo on 8080. Choose another
port if 8081 is occupied.

1. Confirm five sample tasks and 40% completion.
2. Add a task and mark it complete; verify the cards and chart change.
3. Search and try the Open and Complete filters.
4. Export CSV and inspect it.
5. Reload to restore the original sample data.

Stop the server with **Ctrl+C** in the terminal. No R packages, reticulate,
or RStudio Publish button are required for this workflow.

## How it works

`connect_app.py` imports the existing dashboard and exposes a FastAPI object
named `app`. `ui.run_with(app)` attaches NiceGUI. Uvicorn runs that ASGI entry
point, which can also be supplied to Posit Connect. The existing `python main.py`
workflow remains available.

This verifies the entry point locally. Actual Connect compatibility, including
WebSockets, proxy URL paths, authentication, and process routing, must be tested
on the office server. Data still resets on reload and is independent per page.

## Later: publish from the office

Install `rsconnect-python` in the virtual environment and configure your office
Connect server using your organization's normal publishing instructions.
With a configured server nickname, the command has this form:

```text
.venv\Scripts\rsconnect.exe deploy fastapi --name OFFICE_SERVER --entrypoint connect_app:app .
```

Replace `OFFICE_SERVER` with the configured nickname. Never commit API keys.
Review the upload bundle and exclude local environments, logs, and unrelated
files using the deployment tool's exclusion options. Start with one app process
for this in-memory POC and verify interactions before changing process settings.

Community Edition does not include a hosting server. Publishing requires network
access and publishing permission on Connect; this local POC does not bypass that.

## References

- [RStudio version control](https://docs.posit.co/ide/user/ide/guide/tools/version-control.html)
- [Connect FastAPI publishing](https://docs.posit.co/connect/user/fastapi/)

[Back to README](../README.md)

## Ready to publish?

Read [Publishing and hosting](publishing.md) for the required destination, server access, and deployment verification. Running this POC in Community Edition does not create a hosted application.
