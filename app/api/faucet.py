from inspect import indentsize
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app import deps
from app.models.faucet import Faucet as FaucetModel
from app.utils import get_twitter_username, get_platform, validate_url, normalise_query_string
from app.services import faucet_service
from app.crud import faucet_crud
from app.schemes.faucet import Faucet, FaucetNetwork, FaucetAmount, FaucetNetworkMap, FaucetOutList
from typing import List
from app.db.redis import redis_cache
from fastapi.encoders import jsonable_encoder
import json
import os

router = APIRouter()


@router.post("/create", name="")
async def create(url: str, network: str = FaucetNetwork.default, db: Session = Depends(deps.get_db)):

    if validate_url(url) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="None validate URL")

    url = normalise_query_string(url)
    platform = get_platform(url)

    if not platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong platform URL")

    #username = ''
    # if platform == FaucetPlatform.twitter:
    #    username = get_twitter_username(url)

    count = faucet_crud.faucet.get_day_count_by_user(
        db=db, url=url, network=network, platform=platform)
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="dup url, try tomorrow")

    # !! dup record fliter
    obj_in = Faucet(url=url, network=FaucetNetwork[network], platform=platform,
                    amount=FaucetAmount[FaucetNetwork.default].value["num"])
    # print(obj_in)
    item = faucet_crud.faucet.create(db=db, obj_in=obj_in)
    await faucet_service.scrape(platform=platform, id=item.id, url=url, created_at=item.created_at)

    return {"status": item.status}

# response_model=List[FaucetByPlatform]
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
