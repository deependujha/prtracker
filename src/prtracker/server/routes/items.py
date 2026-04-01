# credits: https://github.com/deependujha

# app/routes/items.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_items():
    return {"items": []}


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
