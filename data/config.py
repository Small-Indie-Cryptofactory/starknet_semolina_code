import os
import sys
from pathlib import Path
from loguru import logger


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ETH_RPC = 'https://rpc.ankr.com/eth'

FILES_DIR = os.path.join(ROOT_DIR, 'files')
DEBUG_PATH = os.path.join(FILES_DIR, 'debug.log')
PROXY_PATH = os.path.join(FILES_DIR, 'proxy.txt')
PRIVATE_KEYS_PATH = os.path.join(FILES_DIR, 'private_keys.csv')
SETTINGS_PATH = os.path.join(FILES_DIR, 'settings.json')

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

logger.add(f'{FILES_DIR}/debug.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')
