from starknet_py.net.account.account import Account
from starknet_py.net.client_errors import ClientError
from aiohttp.client_exceptions import ClientConnectorError

from tasks.base import Base
from data.config import logger
from utils.utils import get_explorer_hash_link


class Argent(Base):
    async def wallet_deploy(self, depth=10):
        if depth == 0:
            raise ValueError('Failed to deploy account (argent).')
        wallet_address = self.starknet_client.hex_address
        failed_text = f'Failed to deploy {wallet_address}'
        try:
            key_pair = self.starknet_client.key_pair

            implementation_class_hash, proxy_class_hash, selector, calldata = self.starknet_client.get_wallet_info(
                wallet=self.starknet_client.provider, key_pair=key_pair)

            account_deployment_result = await Account.deploy_account(
                address=self.starknet_client.account.address,
                class_hash=implementation_class_hash,
                salt=key_pair.public_key,
                key_pair=key_pair,
                client=self.starknet_client.starknet_client,
                chain=self.starknet_client.chain_id,
                constructor_calldata=[*calldata],
                auto_estimate=True,
            )

            result = await account_deployment_result.wait_for_acceptance()
            if result:
                tx_hash = await Base.int_to_hex(result.hash)
                msg = (f'Argent wallet: {wallet_address}. Deploy successfully. Tx hash: '
                       f'{get_explorer_hash_link(tx_hash)}')
                return msg
        except (ClientError, ClientConnectorError):
            logger.warning(f'Deploy failed {wallet_address} | Trying again...')
            return await self.wallet_deploy(depth-1)
        except ValueError as err:
            return f'{failed_text}: something went wrong: {err}'
