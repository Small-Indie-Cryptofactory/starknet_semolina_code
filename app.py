import os
import asyncio
from loguru import logger

from client import EthClient
from data.models import Networks
from functions.create_files import create_files
from utils.import_wallets import get_wallets
from generate_wallets.wallet_generator import wallet_create
from generate_wallets.utils import find_wallets_files, find_proxy_file
from deploy.main import deploy_wallet
from utils.utils import check_node_url, sleep_delay, get_lines, get_starknet_actual_gas_price
from data.models import Wallet, Settings


async def start_deploy_wallets():
    text = f'Enter the path to the file with wallets ( address, private_key, seed_phrase[OPTIONAL] ):\n'
    wallets_files = find_wallets_files()
    if wallets_files:
        for number, wallets_file in enumerate(wallets_files, start=1):
            text += f'Press "{number}" if you want to use {"/".join(wallets_file.split("/")[-2:])}\n'
        text += '> '
    else:
        text += '> '
    wallets_path = input(text).strip()

    if not wallets_path:
        await start_deploy_wallets()
    elif 1 <= int(wallets_path) <= len(wallets_files):
        wallets_path = wallets_files[int(wallets_path) - 1]

    if not os.path.exists(wallets_path):
        logger.error(f'File {wallets_path} does not exists')
        return

    text = f'Enter the path to the proxy file. If there is no proxy, press Enter:\n'
    proxies_file = find_proxy_file()
    if proxies_file:
        text += f'Press "Enter" if you want to use {proxies_file}:\n> '
    else:
        text += '> '
    proxies_path = input(text).strip()
    if not proxies_path:
        proxies_path = proxies_file
    if not os.path.exists(proxies_path):
        logger.error(f'File {proxies_path} does not exists')
        return

    proxies_lst = get_lines(proxies_path)
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


if __name__ == '__main__':
    create_files()
    loop = asyncio.new_event_loop()
    print(f'''Select the action:
1) Generate wallet Ethereum/Argent/Braavos
2) Deploy Argent & Braavos wallets
3) Exit''')

    try:
        loop = asyncio.get_event_loop()
        action = int(input('> '))
        if action == 1:
            wallet_create()
        if action == 2:
            loop.run_until_complete(start_deploy_wallets())
        else:
            exit(1)

    except KeyboardInterrupt:
        print()

    except ValueError as err:
        print(err)
