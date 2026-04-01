# credits: https://github.com/deependujha

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from prtracker.server.db import close_db, init_db
from prtracker.server.routes import api, items, views


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # startup
    yield
    await close_db()  # shutdown


app = FastAPI(lifespan=lifespan)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

if not STATIC_DIR.exists():
    raise ValueError(f"Static directory does not exist at: {STATIC_DIR}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# tags will be used in the OpenAPI docs to group endpoints
app.include_router(views.router, prefix="", tags=["views"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(api.router, prefix="/api", tags=["api"])
