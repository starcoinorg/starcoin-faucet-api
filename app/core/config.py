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
    CELERY_REDIS_BROKER_ADDRESS: str = ""
    CELERY_REDIS_BACKEND_ADDRESS: str = ""
    REDIS_DSN: str = ""
    STARCOIN_FAUCET_MYSQL_HOST: str = os.environ['STARCOIN_FAUCET_MYSQL_HOST']
    STARCOIN_FAUCET_MYSQL_PORT: str = os.environ['STARCOIN_FAUCET_MYSQL_PORT']
    STARCOIN_FAUCET_MYSQL_USER: str = os.environ['STARCOIN_FAUCET_MYSQL_USER']
    STARCOIN_FAUCET_MYSQL_PWD: str = os.environ['STARCOIN_FAUCET_MYSQL_PWD']
    STARCOIN_FAUCET_MYSQL_DB: str = os.environ['STARCOIN_FAUCET_MYSQL_DB']
    SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{STARCOIN_FAUCET_MYSQL_USER}:{STARCOIN_FAUCET_MYSQL_PWD}@{STARCOIN_FAUCET_MYSQL_HOST}:{STARCOIN_FAUCET_MYSQL_PORT}/{STARCOIN_FAUCET_MYSQL_DB}?charset=utf8mb4"
    STARCOIN_FAUCET_PRIVATE_KEY_BARNARD: str = os.environ['STARCOIN_FAUCET_PRIVATE_KEY_BARNARD']
    STARCOIN_FAUCET_PRIVATE_KEY_HALLEY: str = os.environ['STARCOIN_FAUCET_PRIVATE_KEY_HALLEY']
    STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA: str = os.environ['STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA']
    DEBUG: bool = os.environ['STARCOIN_FAUCET_DEBUG']
    # ---------------------aws----------------------
    AWS_ACCESS_KEY_ID: str = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY: str = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_REGION: str = os.environ['AWS_REGION']
    AWS_SENDER: str = os.environ['AWS_SENDER']
    AWS_RECIPIENT: str = os.environ['AWS_RECIPIENT']
    AWS_FAUCET_SUBJECT: str = os.environ['AWS_FAUCET_SUBJECT']
    #
    SESSION_SECRET: str = os.environ['SESSION_SECRET']


    class Config:
        case_sensitive = True


settings = Settings()
