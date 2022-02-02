from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
# from app.db.redis import redis_cache
from app.api import faucet

app = FastAPI(title=settings.SERVER_NAME,
              openapi_url=settings.OPENAPI_URL)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)
#
app.include_router(faucet.router, prefix='')
#
# app.add_event_handler("startup", redis_cache.init_cache)
# app.add_event_handler("shutdown", redis_cache.close)
