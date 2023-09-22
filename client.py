import random
from typing import Optional, Union

from loguru import logger
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientHttpProxyError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp_proxy import ProxyConnector
from fake_useragent import UserAgent
from web3 import Web3
from web3.eth import AsyncEth
from eth_account.signers.local import LocalAccount
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.hash.address import compute_address
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.net.client_errors import ClientError
from starknet_py.serialization import TupleDataclass

from data.models import (
    TokenAmount,
    DEFAULT_TOKEN_ABI,
    Tokens,
    Network,
    Networks,
    Transactions,
    Implementations,
    Settings,
)


class StarknetClient:
    chain_id = StarknetChainId.MAINNET

    def __init__(self, private_key: int, account_address: int, proxy: str = '', check_proxy: bool = True):
        self.hex_address = self.value_to_hex(account_address)
        self.key_pair = KeyPair.from_private_key(private_key)
        self.signer = StarkCurveSigner(account_address, self.key_pair, StarknetClient.chain_id)
        self.chain_id = StarknetChainId.MAINNET

        self.starknet_client = None
        self.account = None
        self.cairo_version = None
        self.session = None
        self.connector = None
        self.proxy = proxy

        self.check_proxy = check_proxy
        self.provider = self.get_wallet_provider()

        if self.proxy:
            try:
                if 'http' not in self.proxy:
                    self.proxy = f'http://{self.proxy}'

            except BaseException as err:
                raise ValueError(str(err))

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.proxy:
            await self.session.close()

    async def initialize(self):
        await self.initialize_starknet_client()
        self.account = Account(
            address=int(self.hex_address, 16),
            client=self.starknet_client,
            key_pair=self.key_pair,
            chain=self.chain_id
        )

    async def get_my_ip(self):
        try:
            async with self.session.get("https://ipinfo.io/ip") as response:
                return await response.text()
        except ClientHttpProxyError:
            logger.error('Error occurred while using the proxy.')
            raise

    async def initialize_starknet_client(self):
        settings = Settings()
        if self.proxy:
            self.connector = self.get_session()
            self.session = ClientSession(connector=self.connector)
            if self.check_proxy:
                my_ip = await self.get_my_ip()
                logger.debug(f"Address {self.hex_address}. Current proxy: {self.proxy.split('@')[1].split(':')[0]}. "
                             f"Current IP is: {my_ip}")
            self.starknet_client = FullNodeClient(
                node_url='https://starknet-mainnet.public.blastapi.io',
                session=self.session
            )
            return
        logger.warning(f'Proxy not used')
        node_url = settings.node_url if settings.node_url else 'https://starknet-mainnet.public.blastapi.io'
        self.starknet_client = FullNodeClient(node_url=node_url)

    async def close(self):
        await self.session.close()

    def get_session(self):
        if self.proxy:
            return ProxyConnector.from_url(self.proxy)
        return None

    @staticmethod
    def get_wallet_info(wallet, key_pair):
        if wallet == 'argent_0.3.0':
            implementation_class_hash = Implementations.Argent.contract_address
            proxy_class_hash = int('0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918', 16)
            selector = int('0x79dc0da7c54b95f10aa182ad0a46400db63156920adb65eca2654c0945a463', 16)
            calldata = [key_pair.public_key, 0]
            return implementation_class_hash, proxy_class_hash, selector, calldata
        elif wallet == 'braavos_000.000.011':
            implementation_class_hash = int('0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570', 16)
            proxy_class_hash = int('0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e', 16)
            selector = int('0x02dd76e7ad84dbed81c314ffe5e7a7cacfb8f4836f01af4e913f275f89a3de1a', 16)
            calldata = [key_pair.public_key]
            return implementation_class_hash, proxy_class_hash, selector, calldata

        return None

    def get_wallet_provider(self):
        def calculate_address(wallet_provider, implementation_class_hash, proxy_class_hash, selector, calldata):
            address = compute_address(
                class_hash=proxy_class_hash if wallet_provider != 'argent_0.3.0' else implementation_class_hash,
                constructor_calldata=[implementation_class_hash, selector, len(calldata), *calldata] if
                wallet_provider != 'argent_0.3.0' else [*calldata],
                salt=self.key_pair.public_key
            )
            return address

        providers = ["argent_0.3.0", "braavos_000.000.011"]

        for provider in providers:
            info_tuple = self.get_wallet_info(wallet=provider, key_pair=self.key_pair)
            computed_wallet = calculate_address(provider, *info_tuple)
            if computed_wallet == int(self.hex_address, 16):
                return provider

        return 'Failed to calculate address'

    def value_to_hex(self, value=None) -> Optional[str]:
        if not value:
            return '0x{:064x}'.format(self.account.address)
        return '0x{:064x}'.format(value)

    async def get_decimals(self, token_address: int, depth: int = 10) -> int:
        if depth == 0:
            raise ValueError('Failed to check decimals balance.')
        contract = Contract(
            address=token_address,
            abi=DEFAULT_TOKEN_ABI,
            provider=self.account
        )
        try:
            return int(StarknetClient.get_data(await contract.functions['decimals'].call()))
        except ClientError:
            return await self.get_decimals(token_address, depth-1)

    async def get_balance(self, token_address: int = Tokens.ETH.address, depth: int = 10) -> TokenAmount:
        if depth == 0:
            raise ValueError('Failed to retrieve balance.')
        try:
            return TokenAmount(
                amount=await self.account.get_balance(token_address=token_address, chain_id=StarknetChainId.MAINNET),
                decimals=await self.get_decimals(token_address=token_address),
                wei=True
            )
        except (ClientError, ClientConnectorError):
            return await self.get_balance(token_address, depth-1)

    @staticmethod
    def get_data(info: Union[int, TupleDataclass, tuple, dict]):
        if isinstance(info, int) or isinstance(info, str):
            return info
        elif isinstance(info, TupleDataclass):
            return info.as_tuple()[0]
        elif isinstance(info, tuple):
            return info[0]
        elif isinstance(info, dict):
            return list(info.values())[0]
        return info


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

        self.transactions = Transactions(self)
