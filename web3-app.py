from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime, timezone
from os import environ
from pprint import pprint
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Given a connection to the blockchain, find the latest block and print its
# timestamp.
def get_latest(w3):
    latest_block = datetime.utcfromtimestamp(
        w3.eth.get_block('latest').timestamp
    ).replace(tzinfo=timezone.utc)

    print(latest_block.astimezone().strftime("%B %e, %Y at %r"))

# Retrieve the known accounts for this instance.
def get_accounts(w3):
    print(w3.eth.accounts)

# Show the balance of the first account found.
def get_balance(w3):
    print(Web3.fromWei(w3.eth.get_balance(w3.eth.accounts[0]), 'ether'))
    Web3.eth.account

# Send an ETH amount to a designated address:
def send_eth(w3, to, amount):    
    passphrase = environ.get('ETH_PASSPHRASE')
    if not passphrase:
        print('The ETH_PASSPHRASE environment variable was not set.')
        print('Re-run this script using the Doppler CLI: doppler run -- send Ox...')
        exit(1)
    txn = w3.geth.personal.send_transaction({
        'to': Web3.toChecksumAddress(to),
        'value': w3.toWei(amount, 'ether'),
        'from': w3.geth.personal.list_accounts()[0]
    }, passphrase)
    print(repr(txn))
    
# Retrieve and display a given transaction ID
def get_txn(w3, txn):
    pprint(dict(w3.eth.get_transaction(txn)))

if __name__ == '__main__':
    # Construct a parser with subcommands
    parser = ArgumentParser(description='List of web3 commands')
    subparsers = parser.add_subparsers(help='Get latest block timestamp')
    subparsers.add_parser('latest-block').set_defaults(f=get_latest)
    subparsers.add_parser('accounts').set_defaults(f=get_accounts)
    subparsers.add_parser('balance').set_defaults(f=get_balance)
    sender = subparsers.add_parser('send')
    sender.set_defaults(f=send_eth)
    sender.add_argument('to', help='address to send funds to')
    sender.add_argument('amount', help='quantity of ETH to send')
    viewer = subparsers.add_parser('get-txn')
    viewer.set_defaults(f=get_txn)
    viewer.add_argument('txn', help='transaction ID to fetch')
    args = parser.parse_args()

    # Confirm that a subcommand has been passed
    if 'f' in args:
        # We'll need this connection object for whatever command we end up running
        w3 = Web3(Web3.IPCProvider(Path.home() / '.goerli' / 'geth.ipc'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Run our command function
        if args.f == send_eth:
            args.f(w3, args.to, args.amount)
        elif args.f == get_txn:
            args.f(w3, args.txn)
        else:
            args.f(w3)
    else:
        # No subcommand from the CLI? Print help text
        parser.print_help()
