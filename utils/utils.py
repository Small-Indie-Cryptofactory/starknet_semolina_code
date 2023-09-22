import time
import random
from decimal import Decimal
from typing import Optional, Union
from datetime import datetime, timedelta, timezone

import asyncio
import aiohttp
from loguru import logger
from fake_useragent import UserAgent
from tqdm import tqdm
from data.models import Settings, Wei


def check_node_url(proxies_lst: list):
    settings = Settings()
    if settings.node_url in ['', 'https://starknet-mainnet.public.blastapi.io'] and not proxies_lst:
        logger.warning('\nWe recommend adding the Alchemy/Blast RPC provider to the node_url settings.\n'
                       'Currently, you are not using a proxy and are using a public RPC.\n'
                       'Press Enter if you are sure and want to continue the action.\n'
                       'Press CTRL + C to close program.')
        input()


def randfloat(from_: Union[int, float, str], to_: Union[int, float, str],
              step: Optional[Union[int, float, str]] = None) -> float:
    from_ = Decimal(str(from_))
    to_ = Decimal(str(to_))
    if not step:
        step = 1 / 10 ** (min(from_.as_tuple().exponent, to_.as_tuple().exponent) * -1)

    step = Decimal(str(step))
    rand_int = Decimal(str(random.randint(0, int((to_ - from_) / step))))
    return float(rand_int * step + from_)


def update_dict(modifiable: dict, template: dict, rearrange: bool = True, remove_extra_keys: bool = False) -> dict:
    for key, value in template.items():
        if key not in modifiable:
            modifiable.update({key: value})

        elif isinstance(value, dict):
            modifiable[key] = update_dict(
                modifiable=modifiable[key], template=value, rearrange=rearrange, remove_extra_keys=remove_extra_keys
            )

    if rearrange:
        new_dict = {}
        for key in template.keys():
            new_dict[key] = modifiable[key]

        for key in tuple(set(modifiable) - set(new_dict)):
            new_dict[key] = modifiable[key]

    else:
        new_dict = modifiable.copy()

    if remove_extra_keys:
        for key in tuple(set(modifiable) - set(template)):
            del new_dict[key]

    return new_dict


def unix_to_strtime(unix_time: Union[int, float, str] = None, utc_offset: Optional[int] = None,
                    format: str = '%d.%m.%Y %H:%M:%S') -> str:
    if not unix_time:
        unix_time = time.time()

    if isinstance(unix_time, str):
        unix_time = int(unix_time)

    if utc_offset is None:
        strtime = datetime.fromtimestamp(unix_time)
    elif utc_offset == 0:
        strtime = datetime.utcfromtimestamp(unix_time)
    else:
        strtime = datetime.utcfromtimestamp(unix_time).replace(tzinfo=timezone.utc).astimezone(
            tz=timezone(timedelta(seconds=utc_offset * 60 * 60)))

    return strtime.strftime(format)


def get_explorer_hash_link(tx_hash: str, eth=False):
    if eth:
        return f'https://etherscan.io/tx/{tx_hash}'
    return f'https://starkscan.co/tx/{tx_hash}'


def get_request_headers() -> dict:
    user_agent = UserAgent().chrome
    version = user_agent.split('Chrome/')[1].split('.')[0]
    platform = ['macOS', 'Windows', 'Linux']

    headers = {
        'authority': 'starkgate.starknet.io',
        'sec-ch-ua': f'" Not A;Brand";v="99", "Chromium";v="{version}", "Google Chrome";v="{version}"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'sec-ch-ua-platform': f'"{random.choice(platform)}"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://starkgate.starknet.io/',
        'accept-language': 'pl-PL,pl',
    }

    return headers


async def sleep_delay():
    settings = Settings()
    sleep_time = random.randint(
        settings.sleep_time.from_, settings.sleep_time.to_
    )
    next_action_time = int(time.time()) + int(sleep_time)
    logger.debug(f'I will sleep {sleep_time} second(s). The next closest action will '
                 f'be performed at {unix_to_strtime(next_action_time)}')
    for _ in tqdm(range(sleep_time), desc='Sleeping: ', unit='SEC', colour='GREEN'):
        await asyncio.sleep(1)


def get_lines(path):
    proxies_lst = []
    if path:
        with open(path, encoding='utf-8') as f:
            proxies_lst = list(map(lambda line: line.strip(), filter(lambda line: line.strip(), f.readlines())))
    return proxies_lst


async def get_starknet_actual_gas_price(depth=10):
    if depth == 0:
        raise ConnectionError(f'Not possible receive actual gas_price')
    user_agent = UserAgent().chrome

    url = 'https://alpha-mainnet.starknet.io/feeder_gateway/get_block?blockNumber=latest'

    headers = {
        'authority': 'alpha-mainnet.starknet.io',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'ru-RU,ru;q=0.7',
        'user-agent': user_agent,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with await session.get(
                    url=url,
                    headers=headers,
                    allow_redirects=True
            ) as r:
                result = (await r.json())
                gas_price = Wei(int(result['gas_price'], 16))
                return gas_price
    except:
        return await get_starknet_actual_gas_price(depth - 1)
