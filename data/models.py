import os
import json
from decimal import Decimal
from typing import Optional, Union
from dataclasses import dataclass
from utils.files_utils import read_json

import requests
from web3 import Web3

from data.config import ABIS_DIR, SETTINGS_PATH


# Token-ABI
DEFAULT_TOKEN_ABI = json.load(open(os.path.join(ABIS_DIR, 'default_token_abi.json')))


class Wallet:
    def __init__(self, address: str, private_key: str, proxy: str = ''):
        self.address = int(address, 16)
        self.private_key = int(private_key, 16)
        self.proxy = proxy


class Implementation:
    def __init__(self, name: str, contract_address: str, actual_version: str) -> None:
        self.name = name
        self.contract_address = int(contract_address, 16)
        self.actual_version = actual_version


class Implementations:
    Argent = Implementation(
        name='Argent',
        contract_address='0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003',
        actual_version='0.3.0'
    )
    Braavos = Implementation(
        name='Braavos',
        contract_address='0x05dec330eebf36c8672b60db4a718d44762d3ae6d1333e553197acb47ee5a062',
        actual_version='000.000.011'
    )


class Network:
    def __init__(self, name: str, rpc: str, chain_id: Optional[int] = None, tx_type: int = 0,
                 coin_symbol: Optional[str] = None, explorer: Optional[str] = None
                 ) -> None:
        self.name: str = name.lower()
        self.rpc: str = rpc
        self.chain_id: Optional[int] = chain_id
        self.tx_type: int = tx_type
        self.coin_symbol: Optional[str] = coin_symbol
        self.explorer: Optional[str] = explorer

        if not self.chain_id:
            try:
                self.chain_id = Web3(Web3.HTTPProvider(self.rpc)).eth.chain_id
            except:
                pass

        if not self.coin_symbol:
            try:
                response = requests.get('https://chainid.network/chains.json').json()
                for network in response:
                    if network['chainId'] == self.chain_id:
                        self.coin_symbol = network['nativeCurrency']['symbol']
                        break
            except:
                pass

        if self.coin_symbol:
            self.coin_symbol = self.coin_symbol.upper()


class Networks:
    # Mainnets
    Ethereum = Network(
        name='ethereum',
        rpc='https://rpc.ankr.com/eth/',
        chain_id=1,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://etherscan.io/',
    )


class Token:
    def __init__(self,
                 name: str,
                 address: str,
                 decimal: int,
                 stable: bool = False,
                 token_out_name: str = None,
                 ):
        self.name = name
        self.address = int(address, 16)
        self.hex_address = address
        self.decimal = decimal
        self.stable = stable
        if token_out_name:
            self.token_out_name = token_out_name

    def __str__(self) -> str:
        return f'{self.name}'


class Tokens:
    ETH = Token(
        name='ETH',
        address='0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7',
        decimal=18,
    )


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        """
        A token amount instance.

        :param Union[int, float, str, Decimal] amount: an amount
        :param int decimals: the decimals of the token (18)
        :param bool wei: the 'amount' is specified in Wei (False)
        """
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals


class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)

        return cls._instances[cls]


@dataclass
class FromTo:
    from_: Union[int, float]
    to_: Union[int, float]


class AutoRepr:
    def __repr__(self) -> str:
        values = ('{}={!r}'.format(key, value) for key, value in vars(self).items())
        return '{}({})'.format(self.__class__.__name__, ', '.join(values))


class Unit(AutoRepr):
    """
    An instance of an Ethereum unit.

    Attributes:
        unit (str): a unit name.
        decimals (int): a number of decimals.
        Wei (int): the amount in Wei.
        KWei (Decimal): the amount in KWei.
        MWei (Decimal): the amount in MWei.
        GWei (Decimal): the amount in GWei.
        Szabo (Decimal): the amount in Szabo.
        Finney (Decimal): the amount in Finney.
        Ether (Decimal): the amount in Ether.
        KEther (Decimal): the amount in KEther.
        MEther (Decimal): the amount in MEther.
        GEther (Decimal): the amount in GEther.
        TEther (Decimal): the amount in TEther.

    """
    unit: str
    decimals: int
    Wei: int
    KWei: Decimal
    MWei: Decimal
    GWei: Decimal
    Szabo: Decimal
    Finney: Decimal
    Ether: Decimal
    KEther: Decimal
    MEther: Decimal
    GEther: Decimal
    TEther: Decimal

    def __init__(self, amount: Union[int, float, str, Decimal], unit: str) -> None:
        """
        Initialize the class.

        Args:
            amount (Union[int, float, str, Decimal]): an amount.
            unit (str): a unit name.

        """
        self.unit = unit
        self.decimals = 18
        self.Wei = Web3.to_wei(amount, self.unit)
        self.KWei = Web3.from_wei(self.Wei, 'kwei')
        self.MWei = Web3.from_wei(self.Wei, 'mwei')
        self.GWei = Web3.from_wei(self.Wei, 'gwei')
        self.Szabo = Web3.from_wei(self.Wei, 'szabo')
        self.Finney = Web3.from_wei(self.Wei, 'finney')
        self.Ether = Web3.from_wei(self.Wei, 'ether')
        self.KEther = Web3.from_wei(self.Wei, 'kether')
        self.MEther = Web3.from_wei(self.Wei, 'mether')
        self.GEther = Web3.from_wei(self.Wei, 'gether')
        self.TEther = Web3.from_wei(self.Wei, 'tether')


class Ether(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'ether')


class Wei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'wei')


class GWei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'gwei')


class Transactions:
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def gas_price(w3: Web3) -> Wei:
        return Wei(await w3.eth.gas_price)


class Settings(Singleton, AutoRepr):
    def __init__(self):
        json_data = read_json(path=SETTINGS_PATH)

        self.maximum_gas_price: GWei = GWei(json_data['maximum_gas_price'])
        self.node_url = json_data['node_url']
        self.sleep_time: FromTo = FromTo(from_=json_data['sleep_time']['from'], to_=json_data['sleep_time']['to'])