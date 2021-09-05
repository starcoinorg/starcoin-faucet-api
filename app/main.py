from fastapi import FastAPI
from app.core.config import settings
from app.db.redis import redis_cache
from app.api import faucet

app = FastAPI(title=settings.SERVER_NAME,
              openapi_url=settings.OPENAPI_URL)
#
app.include_router(faucet.router, prefix='')
#
app.add_event_handler("startup", redis_cache.init_cache)
app.add_event_handler("shutdown", redis_cache.close)

