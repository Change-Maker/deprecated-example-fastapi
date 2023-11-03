import os

import aiofiles
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

_WORKING_DIR = os.path.realpath(os.path.dirname(__file__))
_HTML_PATH = os.path.realpath(
    os.path.join(_WORKING_DIR, "../../static_client_tailwindcss/index.html"),
)

router = APIRouter(
    prefix="/tailwindcss",
    tags=["tailwind css"],
)


@router.get("")
async def example_page():
    async with aiofiles.open(_HTML_PATH, "r") as f:
        return HTMLResponse(content=await f.read(), status_code=200)
