import asyncio

from functions.create_files import create_files
from generate_wallets.wallet_generator import wallet_create


if __name__ == '__main__':
    create_files()
    loop = asyncio.new_event_loop()
    print(f'''Select the action:
1) Generate wallet Ethereum/Argent/Braavos
2) Exit 
''')

    try:
        loop = asyncio.get_event_loop()
        action = int(input('> '))
        if action == 1:
            wallet_create()
        else:
            exit(1)

    except KeyboardInterrupt:
        print()

    except ValueError:
        print(f"You didn't enter a number!")
