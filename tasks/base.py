from typing import Optional

import aiohttp
from fake_useragent import UserAgent

from client import StarknetClient


class Base:
    def __init__(self, starknet_client: StarknetClient):
        self.starknet_client = starknet_client

    async def _get_txs(self, account_address: Optional[str] = None, page: int = 1):
        if not account_address:
            account_address = self.starknet_client.hex_address
        headers = {
            'authority': 'api.viewblock.io',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://viewblock.io',
            'referer': 'https://viewblock.io/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent().chrome,
        }

        params = {
            'page': page,
            'network': 'mainnet',
        }

        url = f'https://api.viewblock.io/starknet/contracts/{account_address}/txs'

        async with aiohttp.ClientSession(connector=self.starknet_client.connector) as session:
            async with await session.get(
                    url,
                    params=params,
                    headers=headers
            ) as r:
                result = (await r.json())
                return result['pages'], result['docs']

    async def get_txs(self, account_address: Optional[str] = None) -> list:
        if not account_address:
            account_address = self.starknet_client.hex_address
        page = 1
        txs_lst = []
        pages, txs = await self._get_txs(account_address=account_address, page=page)
        txs_lst += txs
        if pages == 0:
            return []
        while page < pages:
            page += 1
            pages, txs = await self._get_txs(account_address=account_address, page=page)
            txs_lst += txs
        return txs_lst

    async def check_deploy(
            self,
            txs: Optional[list[dict]] = None,
            type_name: list = ('DEPLOY', 'DEPLOY_ACCOUNT'),
    ) -> bool:
        if txs is None:
            txs = await self.get_txs(account_address=self.starknet_client.hex_address)

        if txs:
            for tx in txs:
                try:
                    if tx['type'] in type_name and tx['status'] in ['ACCEPTED_ON_L1', 'ACCEPTED_ON_L2']:
                        return True
                except TypeError:
                    continue
        return False

    @staticmethod
    async def int_to_hex(value):
        if isinstance(value, int):
            return '0x{:064x}'.format(value)
