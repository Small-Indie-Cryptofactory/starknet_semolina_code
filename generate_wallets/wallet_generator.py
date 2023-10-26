import csv
import os
from tqdm import tqdm
from datetime import datetime

from data.config import FILES_DIR
from generate_wallets.wallet import Wallet


class WalletGenerator:
    @staticmethod
    def generate_wallet(provider) -> Wallet:
        return Wallet(provider=provider)


def wallet_create():
    wallets_rows = []

    wallets_count = input('How many wallets to generate: ')
    while not wallets_count.isdigit() or int(wallets_count) <= 0:
        print('The entered value must be an integer and should not be zero or below zero. Please try again...')
        wallets_count = input('How many wallets to generate: ')
    wallets_count = int(wallets_count)

    provider = input('What wallet you want create (argent/braavos/ethereum): ').lower().strip()
    while provider not in ['argent', 'braavos', 'ethereum']:
        print('Only the wallets argent, braavos, and ethereum are available for generation. Please try again...')
        provider = input('What wallet you want create (argent/braavos/ethereum): ').lower().strip()

    for _ in tqdm(range(wallets_count), desc='Creating wallets: ', unit=' wallets', colour='GREEN'):
        wallet = WalletGenerator.generate_wallet(provider)
        wallets_rows.append([wallet.address, wallet.private_key, wallet.seed_phrase])

    filename = f"{provider}_{len(wallets_rows)}_{str(datetime.now()).replace(' ', '_').replace(':', '.')}.csv"

    with open(os.path.join(FILES_DIR, filename), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['address', 'private_key', 'seed'])
        writer.writerows(wallets_rows)
    
    print(f'{provider.capitalize()} wallets successfully created. File - {filename}')
