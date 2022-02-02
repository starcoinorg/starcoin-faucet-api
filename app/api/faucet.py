from inspect import indentsize
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks, Cookie
from sqlalchemy.orm import Session
from app import deps
from app.models.faucet import Faucet as FaucetModel
from app.utils import get_twitter_username, get_address, validate_url, normalise_query_string
from app.crud import faucet_crud
from app.schemes.faucet import Faucet, FaucetNetwork, FaucetAmount, FaucetNetworkMap, FaucetOutList
from loguru import logger
from starcoin.sdk import (utils, client, local_account, auth_key)
from captcha.image import ImageCaptcha
import random
import string
from fastapi.requests import Request
from fastapi.responses import StreamingResponse
import io
from typing import Optional
from starlette.middleware.sessions import SessionMiddleware



router = APIRouter()

def captcha_generator(size: int):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

@router.post("/create", name="")
async def create(request: Request, address: str, captcha: str, network: str = FaucetNetwork.default, db: Session = Depends(deps.get_db)):
    if not request.session["captcha"] or request.session["captcha"] != captcha.upper():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed, invalid captcha")

    address = get_address(address.lower())
    logger.info(f'create address={address}')
    if not address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed, invalid address ( start with 0x, len 34)")

    count = faucet_crud.faucet.get_create_count_by_address(
        db=db, address=address, network=network)
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed, address once a day, try tomorrow")

    # sdk
    cli = client.Client('https://main-seed.starcoin.org')
    exist = cli.is_account_exist(address)
    if not exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed, address doesn't exist")

    token = cli.get_account_token(address, 'STC', 'STC')
    if not token or token <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed, network balance 0")


    # !! dup record fliter
    obj_in = Faucet(address=address, network=FaucetNetwork[network],
                    amount=FaucetAmount[FaucetNetwork.default].value["num"])
    # print(obj_in)
    item = faucet_crud.faucet.create(db=db, obj_in=obj_in)

    return {"status": item.status}

@router.get("/captcha", name="")
def generate_captcha(request: Request):
    image = ImageCaptcha()
    v = captcha_generator(5)
    data = image.generate(v)
    request.session["captcha"] = v
    return StreamingResponse(io.BytesIO(data.getvalue()), media_type="image/png")

# @router.get("/recently", name="")
# async def recently(network: str, db: Session = Depends(deps.get_db)):

#     if not network or network not in FaucetNetworkMap.__members__:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong platform")

#     key = f'recently:{network}'

#     items = await redis_cache.get(key)
#     if items:
#         return json.loads(items)

#     items = faucet_crud.faucet.get_recently_by_network(db=db, network=network)

#     rtn = []
#     for item in items:
#         rtn.append(FaucetOutList(address=item.address, network=item.network, transfered_txn=item.transfered_txn).dict())

#     await redis_cache.set((key), json.dumps(rtn), 2 * 60)

#     return rtn
