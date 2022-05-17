# Getting Started with Web3 and Python

This repository is an accompaniment to the Doppler and Web3 published at ${URL} and all of the code used in the article (and more) is contained in [web3-app.py](./web3-app.py).

You can view the available commands once setup by running:

```sh
python web3-app.py --help
```

## Requirements

- [Alchemy account](https://auth.alchemyapi.io/)
- Python 3
- Geth CLI ([installation docs](https://geth.ethereum.org/docs/install-and-build/installing-geth))

## Setup

The following instructions use [Homebrew](https://brew.sh/) for macOS but can easily be adapted for Linux and Windows.

Install Python3 and Ethereum:

```sh
brew install python
brew tap ethereum/ethereum
brew install ethereum
```

The Geth CLI should now be on your `$PATH`:

```sh
geth version
```

In a background terminal, create a connection to the Goerli test Ethereum network:

```sh
# --syncmode light` downloads block headers without transactions to save disk and memory space
geth --syncmode light --datadir ~/.goerli --goerli
```

Clone the repository:

```sh
git clone https://github.com/DopplerUniversity/python-web3
cd python-web3
```

Then create a virtual environment and install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

Test everything is setup by running:

```sh
python web3-app.py --help
```

## Doppler

Next, we'll [install the Doppler CLI](https://docs.doppler.com/docs/enclave-installation) and [create a Doppler project](https://docs.doppler.com/docs/create-project) for storing the passphrase for your test Ethereum account.

Install the CLI:

```sh
# See https://docs.doppler.com/docs/enclave-installation for other operating systems and environments, e.g. Docker
brew install dopplerhq/cli/doppler
```

Authenticate your machine:

```sh
doppler login
```

Then create the `python-web3` Doppler project:

```sh
doppler projects create python-web3
doppler setup --project python-web3 --config dev
```

## Test Account

The creation of your test account (a locally encrypted file in the `~/.goerli` directory) is protected using a passphrase which must be provided when performing actions such as making a transaction.

[Doppler](https://www.doppler.com/) will be used for storing the passphrase so it can securely injected as an environment variable using the Doppler CLI.

Without a SecretOps platform such as Doppler, storing the passphrase in an unencrypted local file risks that file being [accidentally committed to GitHub](https://twitter.com/nateliason/status/1392086702794149894) with disastrous consequences.


Create a new `ETH_PASSPRASE` secret in Doppler to store your passphrase:

```sh
doppler secrets set ETH_PASSPHRASE
```

Then use the Doppler to inject your passphrase into the Geth CLI command for creating your test account:

```sh
doppler run --command='geth account new --datadir ~/.goerli --password <(echo "$ETH_PASSPHRASE")'
```

Now verify your account has been created by running:

```sh
python web3-app.py accounts
```

## Add Funds

Now add test funds to your new account using the [Goerli Faucet](https://goerlifaucet.com/) where you can request 0.05 Goerli ETH per day.

The Goerli Faucet is an Ethereum faucet built for developers to test and troubleshoot their decentralized application or protocol before going live on Ethereum mainnet.

Once you've requested your 0.05 Goerli ETH, you can verify it's in your account by running:

```sh
python web3-app.py balance
```
## Send Transaction

You'll need an address for sending a transaction which you can get from the [Goerli accounts page](https://goerli.etherscan.io/accounts).

Now use the Doppler CLI to dynamically inject the `ETH_PASSPHRASE` value as an environment variable into the Python process:

```sh
# Replace {ADDRESS} with the public address of the wallet you would like to send funds to e.g. 0xe0a2bd4258d2768837baa26a28fe71dc079f84c7
doppler run -- python web3-app.py send {ADDRESS} 0.01
```

You can then use the returned hash to view the transaction details:

```sh
python web3-app.py get-txn {TRANSACTION_HASH}
```

## Summary

Now you know how to get started building a Python Web3 application using the [Doppler SecretOps platform](https://www.doppler.com/) for secure management of your passphrase.