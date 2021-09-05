from datetime import timedelta, datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.config import settings


class FaucetBase(BaseModel):
    pass

class Faucet(BaseModel):
    network: Optional[str] = Field(None, title="network")
    platform: Optional[str] = Field(None, title="platform")
    url: Optional[str] = Field(None, title="url")
    amount: Optional[str] = Field(0, title="amount")
    
    class Config:
        orm_mode = True

class FaucetCreate(FaucetBase):
    url: Optional[str] = Field(description="3rd party share link")

class FaucetUpdate(FaucetBase):
    amount: Optional[str] = Field(0, title="amount")
    address: Optional[str] = Field(None, title="address")
    status: Optional[str] = Field(0, title="status")
    transferd_at: Optional[datetime] = Field(None, title="transferd_at")
    transferd_txn: Optional[str] = Field(None, title="transferd_txn")

# ---------------- resp -----------------------
class FaucetByPlatform(FaucetBase):
    transfered_txn: str = Field(None, title="transferd_txn")

    class Config:
        orm_mode = True

class FaucetMessage(FaucetBase):
    message: str

# ---------------- enum -----------------------

class FaucetStatus(int, Enum):
    init = 0
    success = 20
    # transfer success
    coin_success = 21
    # 
    fail = 40
    # transfer fail
    coin_fail = 41
    coin_already_transfered = 42

# binding
class FaucetNetwork(str, Enum):
    default = "barnard"
    barnard = "barnard"
    halley = "halley"
    proxima = "proxima"

class FaucetNetworkMap(dict, Enum):
    barnard = {
        "url": "https://barnard-seed.starcoin.org",
        "chainId": 251,
        "senderPrivateKey": settings.STARCOIN_FAUCET_PRIVATE_KEY_BARNARD
    }
    halley = {
        "url": "https://halley-seed.starcoin.org",
        "chainId": 253,
        "senderPrivateKey": settings.STARCOIN_FAUCET_PRIVATE_KEY_HALLEY
    },
    proxima = {
        "url": "https://proxima-seed.starcoin.org",
        "chainId": 252,
        "senderPrivateKey": settings.STARCOIN_FAUCET_PRIVATE_KEY_PROXIMA
    }


day1 = timedelta(days=1)
class FaucetAmount(dict, Enum):
    barnard = { "num":3, "t":"STC", "time": day1, "str": '3 STC / day' }

class FaucetPlatform(str, Enum):
    facebook = "facebook"
    twitter = "twitter"
    