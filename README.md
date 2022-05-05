# python-web3

Get started quickly - please note that you'll need a functional python installation and a running `geth` node for the `web3` library to connect to<sub>[1]</sup>. This command will return the timestamp of the latest minted block:

```console
git clone https://github.com/DopplerUniversity/python-web3
cd python-web3
make latest-block
```

For other script commands, you may run the `script.py` file from the instantiated virtualenv (you can manually create the virtualenv with `make deps`):

```console
./ve/bin/python script.py
```

[1]: https://geth.ethereum.org/docs/getting-started
