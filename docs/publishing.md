# Publishing and hosting

## What "publish to RStudio" means

RStudio Desktop Community Edition is a development environment. You can open this
repository and run Python from its Terminal, but it does not provide a public
hosting service. Its local preview stops when the Python process stops.

| Component | Role in this project |
| --- | --- |
| Personal GitHub repository | Stores the source code and documentation. |
| RStudio Community Edition | Opens the project and provides a terminal to run or deploy it. |
| Python / Uvicorn | Executes the NiceGUI backend. |
| Posit Connect, formerly RStudio Connect | A separate server that can run deployed Python ASGI applications. |
| User's browser | Displays the interface and sends actions to the backend. |

Pushing to GitHub does not deploy this application. A publishing destination must
be selected and configured separately. A personal GitHub repository also does
not imply that a Posit hosting account or Connect server exists.

## Current project status

- The local NiceGUI dashboard and FastAPI entry point are implemented.
- `connect_app:app` has been served locally with Uvicorn and returned the dashboard.
- The task workflow tests pass using NiceGUI's simulated user.
- The RStudio workflow is documented; it has not been verified by controlling the
  RStudio desktop UI.
- No deployment to Posit Connect or another cloud service has been performed.

Local success does not establish compatibility with a particular Connect server.
Connect supports FastAPI/ASGI publishing, but this NiceGUI integration still needs
an end-to-end check on the target installation.

## Option 1: preview with RStudio Community Edition

Follow the [RStudio POC walkthrough](rstudio-poc.md). The backend runs on your
computer and you open `http://127.0.0.1:8081`. No publishing account is needed.
This is useful for demonstrating the application before selecting a host.

## Option 2: publish to office Posit Connect

To proceed, you need:

1. The office Connect server URL and access to it from the publishing computer.
2. A Connect account with publishing permission and an approved authentication setup.
3. A Python version supported by both the server and this project (Python 3.10+).
4. Approval under your organization's normal process to deploy from a personal repo.

If your personal computer cannot reach office Connect, clone or pull this repository
on your office computer and publish from there. RStudio Community Edition does
not bypass network restrictions. Use your organization's approved VPN only if
that is an available way to access the service.

From the project directory, install the publisher into the virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install rsconnect-python
```

Configure the server and credentials using your organization's publishing
instructions. With a configured server nickname, deploy the ASGI entry point:

```powershell
.\.venv\Scripts\rsconnect.exe deploy fastapi --name OFFICE_SERVER --entrypoint connect_app:app .
```

`OFFICE_SERVER` is a placeholder for the configured nickname, not a literal server
name. Keep API keys out of source code, Git commits, documentation, and shared logs.
Review the deployment bundle and exclude local environments and unrelated files
using the publisher's exclusion options; do not assume `.gitignore` controls uploads.

After publishing, check the assigned Connect URL, page assets, task interactions,
CSV download, and access restrictions. For this in-memory POC, start with one app
process and verify session behavior. Check WebSocket connections and URL prefixes
if the page loads but controls do not respond. Use Connect logs to investigate
startup or dependency failures.

Once successfully deployed, the backend runs on the Connect server. Your personal
and office computers can be switched off. The organization or hosting provider
maintains that Connect infrastructure.

## Option 3: personal managed cloud hosting

If office Connect is unavailable and you want a public cloud demonstration, choose
a separate host that supports a persistent Python ASGI process and WebSockets.
An example ASGI start command is:

```sh
python -m uvicorn connect_app:app --host 0.0.0.0 --port "$PORT"
```

This example assumes a Linux shell and a hosting platform that supplies `PORT`.
Use the actual platform's build, port, HTTPS, and account configuration. The build
command for this project is `pip install -r requirements.txt`. No personal cloud
account or service has been configured by this project.

## Data and access

Every page still gets a fresh in-memory list. Publishing does not add persistence,
shared tasks, or accounts. Use managed database storage for saved data and configure
appropriate access controls for office use. These are separate from the local POC.

## Official references

- [Posit Connect FastAPI and ASGI publishing](https://docs.posit.co/connect/user/fastapi/)
- [Python publishing workflow](https://docs.posit.co/connect/user/publishing-cli-apps/)
- [rsconnect-python CLI](https://docs.posit.co/rsconnect-python/commands/deploy/)

[Back to README](../README.md)
