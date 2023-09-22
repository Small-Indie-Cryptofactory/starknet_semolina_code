import csv

from data import config
from utils.files_utils import touch
from typing import Optional

from utils.files_utils import read_json, write_json
from utils.utils import update_dict


def create_files():
    touch(path=config.FILES_DIR)
    touch(path=config.DEBUG_PATH, file=True)
    if touch(path=config.PRIVATE_KEYS_PATH, file=True):
        with open(config.PRIVATE_KEYS_PATH, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['address', 'private_key'])

    try:
        current_settings: Optional[dict] = read_json(path=config.SETTINGS_PATH)
    except FileNotFoundError:
        current_settings = {}

    settings = {
        'maximum_gas_price': 35,
        'node_url': '',
        'sleep_time': {'from': 3600, 'to': 7200},
    }
    write_json(path=config.SETTINGS_PATH, obj=update_dict(modifiable=current_settings, template=settings), indent=2)


create_files()
