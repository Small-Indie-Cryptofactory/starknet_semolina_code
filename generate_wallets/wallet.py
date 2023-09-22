from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.hash.address import compute_address

from client import EthClient
from data.models import Networks
from generate_wallets.seed_phrase_helper.crypto import HDPrivateKey, HDKey
from generate_wallets.utils import grid_key, wallet_to_hex, eip2645_hashing, get_wallet_info


class Wallet:
    def __init__(self, provider):
        self.provider = provider
        self.master_key, self.seed_phrase = HDPrivateKey.master_key_from_entropy()
        if provider == 'argent':
            self.private_key = self.get_argent_private_key(self.seed_phrase)
        elif provider == 'braavos':
            self.private_key = self.get_braavos_private_key(self.seed_phrase)
        if provider == 'ethereum':
            self.private_key = self.get_eth_private_key(self.seed_phrase)
        if provider in ['argent', 'braavos']:
            self.address = self.calculate_address(self.provider, self.private_key)
        else:
            self.eth_client = EthClient(private_key=self.private_key, network=Networks.Ethereum)
            self.address = self.eth_client.account.address

    @staticmethod
    def get_argent_private_key(seed_phrase):
        master_key = HDPrivateKey.master_key_from_mnemonic(seed_phrase)
        root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
        acct_priv_key = root_keys[-1]
        keys = HDKey.from_path(acct_priv_key, '0/0')
        eth_key = keys[-1]._key.to_hex()

        master_key = HDPrivateKey.master_key_from_seed(eth_key)
        root_keys = HDKey.from_path(master_key, "m/44'/9004'/0'/0/0")
        private_key = grid_key(root_keys[-1]._key.to_hex())

        return private_key

    @staticmethod
    def get_braavos_private_key(seed_phrase):
        master_key = HDPrivateKey.master_key_from_mnemonic(seed_phrase)
        root_keys = HDKey.from_path(master_key, "m/44'/9004'/0'/0/0")
        private_key = eip2645_hashing(root_keys[-1]._key.to_hex())

        return private_key

    @staticmethod
    def get_eth_private_key(seed_phrase):
        master_key = HDPrivateKey.master_key_from_mnemonic(seed_phrase)
        root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
        acct_priv_key = root_keys[-1]
        keys = HDKey.from_path(acct_priv_key, '0/0')
        private_key = keys[-1]._key.to_hex()

        return private_key

    @staticmethod
    def calculate_address(provider, private_key):
        private_key = int(private_key, 16)
        key_pair = KeyPair.from_private_key(private_key)

        if provider == 'argent':
            implementation_class_hash, proxy_class_hash, selector, calldata = get_wallet_info(
                wallet='argent', key_pair=key_pair
            )

            address = compute_address(
                class_hash=implementation_class_hash,
                constructor_calldata=[*calldata],
                salt=key_pair.public_key
            )

        elif provider == 'braavos':
            implementation_class_hash, proxy_class_hash, selector, calldata = get_wallet_info(
                wallet='braavos', key_pair=key_pair
            )
        
            address = compute_address(
                class_hash=proxy_class_hash,
                constructor_calldata=[implementation_class_hash, selector, len(calldata), *calldata],
                salt=key_pair.public_key
            )

        else:
            raise ValueError('Wrong provider')

        address_hex = wallet_to_hex(address)
        return address_hex
