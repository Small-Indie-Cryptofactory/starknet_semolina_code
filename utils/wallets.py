import random
import os
from typing import Optional
import csv
from loguru import logger

from data.models import Wallet
from generate_wallets.utils import find_wallets_files, find_proxy_file
from utils.utils import get_lines


def get_wallets_path() -> str:
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
        get_wallets_path()
    elif 1 <= int(wallets_path) <= len(wallets_files):
        wallets_path = wallets_files[int(wallets_path) - 1]

    if not os.path.exists(wallets_path):
        raise FileNotFoundError(f'File {wallets_path} does not exists')
    return wallets_path


def get_proxies_lst() -> list[str]:
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
        return []
    proxies_lst = get_lines(proxies_path)
    return proxies_lst


def get_wallets(path: str, proxies_lst: Optional[list] = None, shuffle: bool = True, skip_first_line: bool = True) -> list[Wallet]:
    wallet_list = []
    with open(path) as f:
        reader = csv.reader(f)
        if skip_first_line:
            next(reader)
        for row in reader:
            if len(row) > 3 or len(row) < 2:
                logger.error(f'Wrong line in {path} file: {row}')
                return []
            wallet_list.append(Wallet(address=row[0], private_key=row[1]))

    for wallet in wallet_list:
        i = 0
        if len(proxies_lst) >= len(wallet_list):
            wallet.proxy = proxies_lst[i]
            i += 1
        else:
            if proxies_lst:
                wallet.proxy = random.choice(proxies_lst)

    if shuffle:
        random.shuffle(wallet_list)
    return wallet_list
