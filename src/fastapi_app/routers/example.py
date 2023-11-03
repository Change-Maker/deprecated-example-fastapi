import io
import os

import aiofiles
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, ORJSONResponse, Response
from loguru import logger
from pydantic import BaseModel

_WORKING_DIR = os.path.realpath(os.path.dirname(__file__))
_EXAMPLE_HTML_PATH = os.path.realpath(
    os.path.join(_WORKING_DIR, "../../static_client/example.html"),
)
_users = []

router = APIRouter(
    prefix="/example",
    tags=["example"],
)


def to_lower_camel(string: str) -> str:
    return (
        "".join(
            [
                s.capitalize() if i > 0 else s
                for i, s in enumerate(string.split("_"))
            ]
        )
    )


class User(BaseModel):
    name: str
    age: int
    is_verified: bool

    class Config:
        alias_generator = to_lower_camel

        # This make User model accept constructing with snake case
        # attributes.
        # Without this, `User(name="alfa", age=14, is_verified=True)`
        # will raise an error which says `isVerified` field is required.
        populate_by_name = True


class Result(BaseModel):
    success: bool = True
    msg: str | None = None


@router.get("")
async def example_page():
    async with aiofiles.open(_EXAMPLE_HTML_PATH, "r") as f:
        return HTMLResponse(content=await f.read(), status_code=200)


@router.get("/orjson-resp")
async def get_orjson_response() -> ORJSONResponse:
    return ORJSONResponse({"a": "alfa", "b": "bravo", "c": "charlie"})


@router.get("/users")
async def get_users() -> list[User]:
    return _users


@router.post("/user")
async def add_user(user: User, resp: Response) -> Result:
    if next((u for u in _users if u.name == user.name), None) is None:
        _users.append(user)
        return Result()
    else:
        resp.status_code = 409  # Conflict.
        return Result(success=False, msg="User already exists.")


@router.post("/txt-file")
async def receive_txt_file(file: UploadFile = File(..., alias="txtFile")):
    out_file_path = os.path.join(_WORKING_DIR, file.filename)
    CHUNK_SIZE = 1024

    # There are two ways to write a file into disk:
    # 1. Load entire file into memory and write to disk.
    # async with aiofiles.open(out_file_path, "wb") as f:
    #     await f.write(await file.read())

    # 2. Write a file in the chunked manner.
    async with aiofiles.open(out_file_path, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)

    return Result()


@router.post("/handle-txt-file")
async def handle_txt_file(file: UploadFile = File(..., alias="txtFile")):
    # Handle a file without saving it into disk.
    buffer = io.BytesIO()
    buffer.write(await file.read())
    buffer.seek(0)  # Set the stream's position back to the start.
    logger.info(f"Handling txt file: {file.filename}")
    buffer.close()

    return Result()
