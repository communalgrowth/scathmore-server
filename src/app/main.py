# scathmore-server, the server for the scathmore game.
# Copyright (C) 2024  Communal Growth, LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from litestar import Controller, Litestar, MediaType, Request, Response, get, post
from litestar.datastructures import State
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.params import Parameter

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dotenv import load_dotenv

load_dotenv()


async def generic_exception_handler(_: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = "Error."
    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=status_code,
    )


class MyController(Controller):
    @post("/scathmore/thunderball/v1/highscore")
    async def score(
        self, state: State, username: str = Parameter(default="", max_length=5)
    ) -> None:
        # Session = async_sessionmaker(bind=state.engine)
        # results = await search_documents(Session, username)
        pass

    @get("/")
    async def hello(self) -> str:
        return "This is the Scathmore server."


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        user = os.environ["SCATHMORE_DB_USER"]
        host = os.environ["SCATHMORE_DB_HOST"]
        port = os.environ["SCATHMORE_DB_PORT"]
        name = os.environ["SCATHMORE_DB_NAME"]
        url = f"postgresql+psycopg://{user}@{host}:{port}/{name}"
        engine = create_async_engine(url)
        setattr(app.state, "engine", engine)
    try:
        yield
    finally:
        await engine.dispose()


app = Litestar(
    route_handlers=[MyController],
    openapi_config=None,
    exception_handlers={
        HTTPException: generic_exception_handler,
    },
    lifespan=[db_connection],
)
