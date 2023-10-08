import random

from loguru import logger

from client import StarknetClient
from upgrade.braavos import BraavosUpgrade
from upgrade.argent import ArgentUpgrade
from utils.utils import sleep_delay
from data.models import Wallet


async def upgrade_wallets(wallets: list[Wallet], shuffle: bool = False):
    if shuffle:
        random.shuffle(wallets)
    for num, wallet in enumerate(wallets, start=1):
        logger.info(f'{num}/{len(wallets)} wallets')
        try:
            async with StarknetClient(
                    private_key=wallet.private_key,
                    account_address=wallet.address,
                    proxy=wallet.proxy
            ) as starknet_client:
                provider = starknet_client.get_wallet_provider()
                if 'braavos' in provider:
                    status = await BraavosUpgrade(starknet_client=starknet_client).braavos_wallet_upgrade()
                elif 'argent' in provider:
                    status = await ArgentUpgrade(starknet_client=starknet_client).argent_wallet_upgrade()
                else:
                    logger.warning(f'Wallet provider for {wallet.address} not found. '
                                   f'Actual wallet provider -> {provider if provider else "Nothing..."}')
                    continue

            if 'Failed' in status:
                logger.error(status)
            elif 'already have' in status:
                logger.warning(status)
            else:
                logger.success(status)
                if num == len(wallets):
                    logger.success(f'Upgrade successfully completed with {len(wallets)} wallets')
                    continue
                await sleep_delay()

        except BaseException as err:
            logger.error(err)
            continue
