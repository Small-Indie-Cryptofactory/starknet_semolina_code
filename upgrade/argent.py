from loguru import logger
from starknet_py.contract import Contract
from starknet_py.net.client_errors import ClientError
from aiohttp.client_exceptions import ClientConnectorError

from tasks.base import Base
from utils.utils import get_explorer_hash_link
from data.models import Implementations, ARGENT_WALLET


class ArgentUpgrade(Base):
    implementation = Implementations.Argent

    async def _get_impl_version(self, contract, depth=10):
        if depth == 0:
            return (f'Failed | Not possible receive impl_version for argent wallet'
                    f'{self.starknet_client.hex_address}. Starknet nodes problem.')
        try:
            impl_version = await contract.functions['getVersion'].call()
            if type(impl_version) is tuple:
                impl_version = bytes.fromhex(hex(impl_version[0])[2:]).decode('utf-8')
            else:
                impl_version = bytes.fromhex(hex(impl_version.as_tuple()[0])[2:]).decode('utf-8')
            return impl_version
        except (ClientError, ClientConnectorError):
            return await self._get_impl_version(contract, depth-1)

    async def argent_wallet_upgrade(self, depth=10):
        """ Upgrade argent wallet """

        if depth == 0:
            return (f'Failed update -> "The server encountered a temporary error and could not complete your request"'
                    f' Wallet {self.starknet_client.hex_address}')

        failed_text = f'Failed argent upgrade, wallet: {self.starknet_client.hex_address}'
        try:

            wallet_contract = Contract(
                address=self.starknet_client.account.address,
                abi=ARGENT_WALLET,
                provider=self.starknet_client.account
            )

            impl_version = await self._get_impl_version(wallet_contract)

            if 'Failed' in str(impl_version):
                return impl_version

            if impl_version == ArgentUpgrade.implementation.actual_version:
                return f'Argent wallet {self.starknet_client.hex_address} already have actual version {impl_version}'
            else:
                upgrade_call = wallet_contract.functions['upgrade'].prepare(
                    implementation=ArgentUpgrade.implementation.contract_address,
                    calldata=[0]
                )
                response = await self.starknet_client.account.execute(
                    calls=[upgrade_call],
                    auto_estimate=True
                )
                tx_hash = self.starknet_client.value_to_hex(response.transaction_hash)
                tx_res = await self.starknet_client.account.client.wait_for_tx(
                    response.transaction_hash
                )
                tx_status = tx_res.finality_status.value
                return (f'Argent wallet {self.starknet_client.hex_address} successfully upgrade | '
                        f'tx: {get_explorer_hash_link(tx_hash)} | status: {tx_status}')

        except (ClientError, ClientConnectorError):
            logger.error(f'Something wrong with server response. Attempts remaining: {depth}')
            return self.argent_wallet_upgrade(depth-1)
        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'
