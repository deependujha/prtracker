# credits: https://github.com/deependujha

from pathlib import Path

from fastapi.templating import Jinja2Templates

ROOT_PROJECT_DIR = Path(__file__).resolve().parent.parent

UI_DIR = ROOT_PROJECT_DIR / "ui"

if not UI_DIR.exists():
    raise ValueError(f"UI directory does not exist at: {UI_DIR}")

templates = Jinja2Templates(directory=UI_DIR)
