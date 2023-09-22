import random
from typing import Optional

from web3 import Web3
from web3.eth import AsyncEth
from fake_useragent import UserAgent
from eth_account.signers.local import LocalAccount

from data.models import (
    Network,
    Networks,
)


class EthClient:
    network: Network
    account: Optional[LocalAccount]
    w3: Web3

    def __init__(self, private_key: Optional[str] = None, network: Network = Networks.Ethereum) -> None:
        self.network = network
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome
        }
        self.w3 = Web3(
            provider=Web3.AsyncHTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'headers': self.headers}
            ),
            modules={'eth': (AsyncEth,)},
            middlewares=[]
        )
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key=private_key)
        else:
            self.account = self.w3.eth.account.create(extra_entropy=str(random.randint(1, 999_999_999)))
