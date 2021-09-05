from starcoin import starcoin_types as types
from starcoin import starcoin_stdlib as stdlib
from starcoin import serde_types as st
from starcoin.sdk import (utils, client, local_account, auth_key)
from starcoin.sdk.receipt_identifier import ReceiptIdentifier
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
import time
import typing
from loguru import logger

def transfer(cli: client.Client, sender: local_account.LocalAccount, receiver: types.AccountAddress, amount: st.uint128, chain_id: st.uint8) -> str:
    seq_num = cli.get_account_sequence(
        "0x"+sender.account_address.bcs_serialize().hex())
    script = stdlib.encode_peer_to_peer_v2_script_function(
        token_type=utils.currency_code("STC"),
        payee=receiver,
        amount=amount,
    )
    node_info = cli.node_info()
    now_seconds = int(node_info.get('now_seconds'))
    # expired after 12 hours
    expiration_timestamp_secs = now_seconds + 43200
    raw_txn = types.RawTransaction(
        sender=sender.account_address,
        sequence_number=seq_num,
        payload=script,
        max_gas_amount=10000000,
        gas_unit_price=1,
        gas_token_code="0x1::STC::STC",
        expiration_timestamp_secs=expiration_timestamp_secs,
        chain_id=types.ChainId(chain_id),
    )

    txn = sender.sign(raw_txn)
    rtn = cli.submit(txn)
    logger.info(f'transfer txn: {rtn}')
    # print(cli.submit(txn))
    # JsonResponseError('Response:{"jsonrpc":"2.0","error":{"code":-49998,"message":"Transaction error (Call txn err: Transaction execution error (Execution error: status SEQUENCE_NUMBER_TOO_OLD of type Validation)..)","data":{"Discard":{"status_code":"3","status_code_name":"SEQUENCE_NUMBER_TOO_OLD"}}},"id":"sdk-client"}\n')
    return rtn

if __name__ == "__main__":
    cli = client.Client("https://barnard-seed.starcoin.org")
    chain_id = 251

    # NanoSTC (1 STC = 1000000000 NanoSTC)
    amount = 1024

    sender_private_key = ""

    reciever_address = "0x4c7afc223df1d47072194dcefe26a445"

    # sender
    private_key = Ed25519PrivateKey.from_private_bytes(
        bytes.fromhex(sender_private_key[2:]))
    sender = local_account.LocalAccount(private_key)

    # reciver
    reciver = types.AccountAddress.from_hex(reciever_address[2:])

    transfer(cli, sender, reciver, amount, chain_id)