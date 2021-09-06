from app.schemes.faucet import FaucetNetwork, FaucetNetworkMap
from sys import platform
from app.crud import faucet_crud
from celery import Celery
from app.core.config import settings
from loguru import logger
import twint
import os
from datetime import datetime, timedelta
import csv
from urllib.parse import urlparse
from app.utils import get_address, normalise_url_without_query, get_twitter_username
from app.core import celeryconfig

celery_app = Celery("celery",
                    backend=settings.CELERY_REDIS_BACKEND_ADDRESS,
                    broker=settings.CELERY_REDIS_BROKER_ADDRESS)                  
celery_app.config_from_object(celeryconfig)

# !!! it's a hack way of tweet scrape, iter user's tweets in one day to find the right one ( limit by twint)
@celery_app.task(bind=True, default_retry_delay=1.1 * 60, max_rettries=3)
def scrape_twitter(self, id, url, created_at):
    logger.info("scrape_twitter")

    # twint
    username = get_twitter_username(url)
    filename = username + '_tweets.csv'
    since = datetime.fromtimestamp(created_at).date()
    until = datetime.fromtimestamp(created_at).date() + timedelta(days=1)
    c = twint.Config()
    c.Username = username
    #c.Debug=True
    c.Store_csv = True 
    c.Output = filename 
    c.Since = since.strftime("%Y-%m-%d")
    c.Until = until.strftime("%Y-%m-%d")
    twint.run.Search(c)

    # file
    address = get_address_from_csv(url, filename)
    logger.info('id since address : {} {} {}'.format(id, since.strftime("%Y-%m-%d"), address))

    # db
    from app.db.session import SessionLocal
    from app.schemes.faucet import FaucetUpdate, FaucetStatus
    #status = FaucetStatus.success.value if address else FaucetStatus.fail.value
    with SessionLocal() as db:
        faucet = faucet_crud.faucet.get(db, id=id)
        if not faucet:
            return False, id, "missing faucet"

        if faucet.status == FaucetStatus.success.value:
            return False, id, "already tranfer"

        if not address:
            faucet_crud.faucet.update(db, db_obj=faucet,obj_in={"status": FaucetStatus.fail.value})
            return False, id, "none address found"

        count = faucet_crud.faucet.get_day_count_by_address(db=db, network=faucet.network, address=address, since=datetime.fromtimestamp(created_at))
        logger.info(f'address count:{count} {datetime.fromtimestamp(created_at)} {faucet.platform}')
        if count > 0:
            faucet_crud.faucet.update(db, db_obj=faucet,obj_in={"status": FaucetStatus.coin_already_transfered.value})
            return False, id, "address already transfer"

        # coin transfer
        try:    
            txn = p2p_tranfer(faucet.network, address, faucet.amount)
            logger.info(f'id since address : {txn}')
            logger.info({"address": address, "status": FaucetStatus.success.value, "transfered_txn": txn, "transafered_at": datetime.now() })
            faucet_crud.faucet.update(db, db_obj=faucet,obj_in={"address": address, "status": FaucetStatus.success.value, "transfered_txn": txn, "transfered_at": datetime.now() })
        except Exception as exc:
            logger.exception(f"{faucet.id} coin error")
            faucet_crud.faucet.update(db, db_obj=faucet,obj_in={"status": FaucetStatus.coin_fail.value})
            raise self.retry(exc=exc)

    # gc
    if os.path.exists(filename):
        os.remove(filename)

    return True, id, "success"


def p2p_tranfer(network ,address, amount):
    if not address or not amount:
        raise Exception('wrong args')

    from starcoin import starcoin_types as types
    from starcoin import starcoin_stdlib as stdlib
    from starcoin import serde_types as st
    from starcoin.sdk import (utils, client, local_account, auth_key)
    from starcoin.sdk.receipt_identifier import ReceiptIdentifier
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey)
    from app.sdk import transfer

    cnf = FaucetNetworkMap[network]
    cli = client.Client(cnf.value['url'])
    chain_id = cnf.value['chainId']
    sender_private_key = cnf.value['senderPrivateKey']

    # NanoSTC (1 STC = 1000000000 NanoSTC)
    # 
    # amount = amount * (1000000000)
    # reciever_address = address
    # debug
    # !!! debug
    if settings.DEBUG:
        amount = 1024 # 
        reciever_address = "0x4c7afc223df1d47072194dcefe26a445"
    else:
        amount = amount * 1000000000
        reciever_address = address

    # sender
    private_key = Ed25519PrivateKey.from_private_bytes(
        bytes.fromhex(sender_private_key[2:]))
    sender = local_account.LocalAccount(private_key)
    # reciver
    reciver = types.AccountAddress.from_hex(reciever_address[2:])
    return transfer(cli, sender, reciver, amount, chain_id)


def get_address_from_csv(url, filename):
    if not os.path.exists(filename):
        return ''

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for t in datareader:
            day = t[3]
            tweet = t[10]
            tweet_url = t[20]
            if tweet_url == "link":
                continue

            # !!! tricky, only match tweet path ( twint api does not have a query)
            if normalise_url_without_query(url) != normalise_url_without_query(tweet_url):
                logger.info(f"url doesn't match {normalise_url_without_query(url)} {normalise_url_without_query(tweet_url)}")
                continue

            address = get_address(tweet)
            logger.info(f'get adderss:{t} {address}')
            break

    return address
    