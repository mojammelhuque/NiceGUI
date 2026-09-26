"""ASGI entry point for Uvicorn and future Posit Connect deployment."""
from fastapi import FastAPI
from nicegui import ui

import main  # Register the page without starting the standalone server.

app = FastAPI()
ui.run_with(app, title='Focus Desk - NiceGUI')
