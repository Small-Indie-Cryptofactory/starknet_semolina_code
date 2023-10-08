import asyncio
from loguru import logger

from client import EthClient
from data.models import Networks
from functions.create_files import create_files
from utils.wallets import get_wallets, get_wallets_path, get_proxies_lst
from generate_wallets.wallet_generator import wallet_create
from deploy.main import deploy_wallet
from utils.utils import check_node_url, sleep_delay, get_starknet_actual_gas_price
from data.models import Wallet, Settings
from upgrade.main import upgrade_wallets


async def start_deploy_wallets():
    wallets_path = get_wallets_path()
    proxies_lst = get_proxies_lst()

    wallets: list[Wallet] = get_wallets(path=wallets_path, proxies_lst=proxies_lst)
    check_node_url(proxies_lst=proxies_lst)
    settings = Settings()

    if not wallets:
        logger.error(f'Problem with wallets import')
        return

    number_of_wallets = len(wallets)
    wallets_with_errors = []

    for wallet_number, wallet in enumerate(wallets, start=1):
        eth_client = EthClient(network=Networks.Ethereum)
        gas_price = await eth_client.transactions.gas_price(w3=eth_client.w3)
        starknet_gas_price = await get_starknet_actual_gas_price()
        while gas_price.GWei > settings.maximum_gas_price.GWei or starknet_gas_price.GWei > starknet_gas_price.GWei:
            logger.warning(f'Current gas price is too high: ETH {gas_price.GWei} or '
                         f'Starknet {starknet_gas_price.GWei} > {settings.maximum_gas_price.GWei}! Sleep 10 minutes...')
            await asyncio.sleep(600)
            gas_price = await eth_client.transactions.gas_price(w3=eth_client.w3)
            starknet_gas_price = await get_starknet_actual_gas_price()

        logger.info(f'({wallet_number}/{number_of_wallets}) Start deploy wallet')
        result = await deploy_wallet(wallet)
        if 'Failed' in result:
            logger.error(result)
            wallets_with_errors.append(wallet.address)
        elif 'already deployed' in result:
            logger.warning(result)
        else:
            logger.success(result)
        if any(message in result for message in ['already deployed', 'Minimum deploy', 'Failed']):
            continue

        if wallet_number >= number_of_wallets:
            break

        await sleep_delay()

    logger.success(f'Deploy actions finished')

    if wallets_with_errors:
        logger.warning('Wallets with errors:')
        for wallet_with_errors in wallets_with_errors:
            logger.warning(wallet_with_errors)


async def upgrade_all_wallets():
    wallets_path = get_wallets_path()
    proxies_lst = get_proxies_lst()

    wallets: list[Wallet] = get_wallets(path=wallets_path, proxies_lst=proxies_lst)
    check_node_url(proxies_lst=proxies_lst)

    if not wallets:
        logger.error(f'Problem with wallets import')
        return

    await upgrade_wallets(wallets, shuffle=True)


if __name__ == '__main__':
    create_files()
    loop = asyncio.new_event_loop()
    print(f'''Select the action:
1) Generate wallet Ethereum/Argent/Braavos
2) Deploy Argent & Braavos wallets
3) Upgrade all wallets
4) Exit''')

    try:
        loop = asyncio.get_event_loop()
        action = int(input('> '))
        if action == 1:
            wallet_create()
        if action == 2:
            loop.run_until_complete(start_deploy_wallets())
        elif action == 3:
            loop.run_until_complete(upgrade_all_wallets())
        else:
            exit(1)

    except KeyboardInterrupt:
        print()

    except ValueError as err:
        print(err)

    except FileNotFoundError as err:
        print(err)
