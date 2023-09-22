import hashlib
import os
from typing import Optional
from starknet_py.hash.selector import get_selector_from_name

from data.models import Implementations
from data.config import FILES_DIR


def get_wallet_info(wallet, key_pair):
    if wallet == 'argent':
        implementation_class_hash = Implementations.Argent.contract_address
        proxy_class_hash = int('0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918', 16)
        selector = get_selector_from_name('initializer')
        calldata = [key_pair.public_key, 0]
        return implementation_class_hash, proxy_class_hash, selector, calldata
    elif wallet == 'braavos':
        implementation_class_hash = int('0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570', 16)
        proxy_class_hash = int('0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e', 16)
        selector = get_selector_from_name('initializer')
        calldata = [key_pair.public_key]
        return implementation_class_hash, proxy_class_hash, selector, calldata
    return None


def wallet_to_hex(value: int):
    if isinstance(value, int):
        return '0x{:064x}'.format(value)


def concat(a, b):
    return a + b


def arrayify(hex_string_or_big_number_or_arrayish):
    try:
        value = int(hex_string_or_big_number_or_arrayish)
    except ValueError:
        value = int(hex_string_or_big_number_or_arrayish, 16)

    if value == 0:
        return [0]

    hex_v = hex(value)[2:]

    if len(hex_v) % 2 != 0:
        hex_v = "0" + hex_v

    result = []
    for i in range(len(hex_v) // 2):
        offset = i * 2
        result.append(int(hex_v[offset:offset + 2], 16))

    return result


def hash_key_with_index(key, index):
    payload = concat(arrayify(key), arrayify(index))
    payload_hash = get_payload_hash(payload)
    return int(payload_hash, 16)


def grid_key(key_seed):
    KEY_VALUE_LIMIT = 0x800000000000010ffffffffffffffffb781126dcae7b2321e66a241adc64d2f
    SHA256_EC_MAX_DIGEST = 0x10000000000000000000000000000000000000000000000000000000000000000

    max_allowed_val = SHA256_EC_MAX_DIGEST - (SHA256_EC_MAX_DIGEST % KEY_VALUE_LIMIT)
    i = 0
    key = 0

    while True:
        key = hash_key_with_index(key_seed, i)
        i += 1
        if key <= max_allowed_val:
            break

    res = hex(abs(key % KEY_VALUE_LIMIT))
    return res


def get_payload_hash(payload):
    m = hashlib.sha256()

    for value in payload:
        hex_value = hex(value)[2::]
        if len(hex_value) == 1:
            hex_value = "0" + hex_value
        m.update(bytes.fromhex(hex_value))

    return m.hexdigest()


def eip2645_hashing(key0):
    N = 2 ** 256
    STARK_CURVE_ORDER = 0x800000000000010FFFFFFFFFFFFFFFFB781126DCAE7B2321E66A241ADC64D2F
    N_MINUS_N = N - (N % STARK_CURVE_ORDER)

    i = 0
    while True:
        x = concat(arrayify(key0), arrayify(i))
        key = int(get_payload_hash(x), 16)

        if key < N_MINUS_N:
            return hex(key % STARK_CURVE_ORDER)
        i += 1


def find_proxy_file(files_dir: str = FILES_DIR) -> Optional[str]:
    files = os.listdir(files_dir)
    files = list(filter(lambda file: file.startswith('proxy') and file.split('.')[-1] == 'txt', files))
    file_name_ctime_dict = {}
    for file in files:
        absolute_path = os.path.join(files_dir, file)
        file_name_ctime_dict[absolute_path] = os.path.getctime(absolute_path)
    sorted_dict = dict(sorted(file_name_ctime_dict.items(), key=lambda item: item[1]))
    if sorted_dict:
        return list(sorted_dict.keys())[0]


def find_wallets_files(files_dir: str = FILES_DIR) -> Optional[list[str]]:
    files = os.listdir(files_dir)
    files = list(filter(
        lambda file: (file.startswith('argent') or file.startswith('braavos') or file.startswith('private')) \
                     and file.split('.')[-1] == 'csv',
        files)
    )
    file_name_ctime_dict = {}
    for file in files:
        absolute_path = os.path.join(files_dir, file)
        file_name_ctime_dict[absolute_path] = os.path.getctime(absolute_path)
    sorted_dict = dict(sorted(file_name_ctime_dict.items(), key=lambda item: item[1]))
    if sorted_dict:
        return list(sorted_dict.keys())
