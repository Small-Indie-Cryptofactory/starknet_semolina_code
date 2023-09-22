from loguru import logger

from client import StarknetClient
from deploy.argent import Argent
from deploy.braavos import Braavos
from data.models import Wallet, Tokens, Ether


async def deploy_wallet(wallet: Wallet):
    async with StarknetClient(
            private_key=wallet.private_key,
            account_address=wallet.address,
            proxy=wallet.proxy
    ) as starknet_client:
        balance = await starknet_client.get_balance(Tokens.ETH.address)
        argent = Argent(starknet_client=starknet_client)
        braavos = Braavos(starknet_client=starknet_client)
        min_balance = Ether(0.001)

        if starknet_client.provider == 'argent_0.3.0':
            if await argent.check_deploy():
                status = f'Wallet {starknet_client.hex_address} already deployed'
            else:
                if balance.Wei < min_balance.Wei:
                    status = f'Failed | Minimum deploy balance must be {min_balance.Ether} ETH! ' \
                             f'Wallet: {starknet_client.hex_address}, actual ETH balance: {balance.Ether}'
                else:
                    logger.info(f'Starting account deploy, wallet: {starknet_client.hex_address}')
                    status = await argent.wallet_deploy()

        elif starknet_client.provider == 'braavos_000.000.011':
            if await braavos.check_deploy():
                status = f'Wallet {starknet_client.hex_address} already deployed'
            else:
                if balance.Wei < min_balance.Wei:
                    status = f'Failed | Minimum deploy balance must be {min_balance.Ether} ETH! ' \
                             f'Wallet: {starknet_client.hex_address}, actual ETH balance: {balance.Ether}'
                else:
                    logger.info(f'Starting account deploy, wallet: {starknet_client.hex_address}')
                    status = await braavos.wallet_deploy()

        else:
            status = (f'Failed for {starknet_client.hex_address}. We only support deployments for argent version '
                      f'0.3.0 and braavos version 000.000.011.')

        return status
