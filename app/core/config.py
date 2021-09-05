import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator, RedisDsn
import os

class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    SECRET_KEY: str = "ee650f31c9c82513414602f1d944416c246944ee6f64cf95376361b392d97e1c"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = 'starcoin-faucet'
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    SERVER_HOST: AnyHttpUrl = 'http://0.0.0.0'

    # -------------------------------------------
    OPENAPI_URL: str = f"{API_V1}/api.json"
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    REDIS_PREFIX: str = "faucet:"
    CELERY_REDIS_BROKER_ADDRESS: str = os.environ['STARCOIN_FAUCET_CELERY_REDIS_BROKER_ADDRESS'] 
    CELERY_REDIS_BACKEND_ADDRESS: str = os.environ['STARCOIN_FAUCET_CELERY_REDIS_BACKEND_ADDRESS']
    REDIS_DSN: str = os.environ['STARCOIN_FAUCET_REDIS_DSN'] 
    SQLALCHEMY_DATABASE_URI = os.environ['STARCOIN_FAUCET_SQLALCHEMY_DATABASE_URI'] 
    STARCOIN_FAUCET_PRIVATE_KEY_BARNARD: str = os.environ['STARCOIN_FAUCET_SQLALCHEMY_DATABASE_URI']
    STARCOIN_FAUCET_PRIVATE_KEY_HALLEY: str = os.environ['STARCOIN_FAUCET_PRIVATE_KEY_HALLEY']
    STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA: str = os.environ['STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA']
    DEBUG: bool = os.environ['STARCOIN_FAUCET_DEBUG'] 

    class Config:
        case_sensitive = True

settings = Settings()

