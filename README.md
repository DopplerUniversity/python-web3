# Python Web3 sample app using Doppler for managing secrets

This repository is an accompaniment to the Doppler and Web3 published at ${URL}.
## Prerequisites

- Python 3
- Geth CLI ([installation docs](https://geth.ethereum.org/docs/install-and-build/installing-geth))

## Setup

The following instructions use homebrew for macOS but can easily be adapted for Linux and Windows.

Ensure Python3 and Ethereum are installed via brew:

```sh
brew install python
brew tap ethereum/ethereum
brew install ethereum
```

The Geth CLI should now be on your `$PATH`:

```sh
geth version
```

Clone the repository:

```sh
git clone https://github.com/DopplerUniversity/python-web3
cd python-web3
```

Then create and activate the virtual environment so the `web3` Python package can be installed:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

> NOTE: If using Windows, use the [Python venv docs](https://docs.python.org/3/library/venv.html) to create and activate your virtual environment in the Terminal or PowerShell.

## Geth

Sync only the most recent block headers from the historical ledger of the blockchain by running:

```sh
geth --syncmode light --datadir ~/.goerli --goerli
```

To create your test account, enter the Geth console by running:

```sh
geth --datadir ~/.goerli attach
```

Then run the following commands:

```
personal.newAccount()
personal.listAccounts
```

Geth is now setup and ready to go!

## Doppler

[Install the Doppler CLI](https://docs.doppler.com/docs/enclave-installation):

```sh
# See https://docs.doppler.com/docs/enclave-installation for other operating systems and environments, e.g. Docker
brew install dopplerhq/cli/doppler
```

 Ensure the Doppler CLI has been authenticated by running:

```sh
doppler login
```

Then create the `python-web3` Doppler project:

```sh
doppler projects create python-web3
doppler setup --project python-web3 --config dev
```

## Configuration

In order for our Python web3 application to function, it needs the passphrase that you set when creating your local Geth account.

This is a perfect use case for Doppler as you definitely don't want to hard-code it or leave it sitting in an unencrypted file where it could be [accidentally committed to GitHub](https://twitter.com/nateliason/status/1392086702794149894) with disastrous consequences.

Create a new secret in Doppler to store your passphrase:

```sh
doppler secrets set ETH_PASSPHRASE
```

## Usage

To view the available commands, run:

```sh
python web3-app.py -h
```

We can view our accounts and balance:
```sh
python web3-app.py accounts
python web3-app.py balance
```

But to send a transaction, we'll need our passphrase which is where the Doppler CLI comes in by injecting the `ETH_PASSPHRASE` as an environment variable:

```sh
# Replace {ADDRESS} with the public address of the wallet you would like to send funds to, e.g. 0x...
doppler run -- python web3-app.py send {ADDRESS} 0.01
```

You can then use the returned transaction hash to look it up on the blockchain:

```sh
python web3-app.py get-txn {TRANSACTION_HASH}
```
