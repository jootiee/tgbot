import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import router
from core.models import db_helper, Base


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await db_helper.engine.dispose()


app = FastAPI(title='TASK', lifespan=lifespan)
app.include_router(router=router)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0")
    uvicorn.run(app)
