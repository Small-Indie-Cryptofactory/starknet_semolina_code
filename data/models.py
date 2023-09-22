from typing import Optional
import requests
from web3 import Web3


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
        contract_address='0x5dec330eebf36c8672b60db4a718d44762d3ae6d1333e553197acb47ee5a062',
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

    Arbitrum = Network(
        name='arbitrum',
        rpc='https://rpc.ankr.com/arbitrum/',
        chain_id=42161,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://arbiscan.io/',
    )

    Optimism = Network(
        name='optimism',
        rpc='https://rpc.ankr.com/optimism/',
        chain_id=10,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://optimistic.etherscan.io/',
    )

    # Testnets
    Goerli = Network(
        name='goerli',
        rpc='https://rpc.ankr.com/eth_goerli/',
        chain_id=5,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://goerli.etherscan.io/',
    )
