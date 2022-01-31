from inspect import indentsize
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app import deps
from app.models.faucet import Faucet as FaucetModel
from app.utils import get_twitter_username, get_address, validate_url, normalise_query_string
from app.crud import faucet_crud
from app.schemes.faucet import Faucet, FaucetNetwork, FaucetAmount, FaucetNetworkMap, FaucetOutList
from loguru import logger
from starcoin.sdk import (utils, client, local_account, auth_key)

router = APIRouter()


@router.post("/create", name="")
async def create(url: str, network: str = FaucetNetwork.default, db: Session = Depends(deps.get_db)):

    url = url.lower()
    address = get_address(url)
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
    cnf = FaucetNetworkMap[network]
    cli = client.Client(cnf.value['url'])
    chain_id = cnf.value['chainId']
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
