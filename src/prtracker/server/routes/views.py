# credits: https://github.com/deependujha

from fastapi import APIRouter, Request

from prtracker.server.templates import templates

router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router.get("/htmx")
def htmx(request: Request):
    return templates.TemplateResponse(request=request, name="partials/love.html", context={"name": "priya"})
