from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from legalaid.chat import models as chat_models  
from legalaid.chat.routes import chat_router
from legalaid.database.db import Base, engine, ensure_postgres_database
from legalaid.database.setting import setting
from legalaid.user import models as user_models  
from legalaid.user.routes import user_routes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_postgres_database(setting.DB_CONNECTION)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="LegalAid", lifespan=lifespan)
_session_secret = setting.SECRET_KEY or "dev-secret-set-SECRET_KEY-in-production"
app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
    session_cookie="legalaid_session",
    same_site="lax",
)


@app.get("/")
async def root():
    return RedirectResponse(url="/user/auth", status_code=302)


app.include_router(user_routes, prefix="/user", tags=["user"])
app.include_router(chat_router, tags=["chat"])


def main() -> None:
    import uvicorn

    package_root = Path(__file__).resolve().parent
    uvicorn.run(
        "legalaid.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(package_root)],
    )


if __name__ == "__main__":
    main()
