import random
from typing import Optional
import csv
from loguru import logger

from data.models import Wallet


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
