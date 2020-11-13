import argparse
import json
import os

from decouple import config
import requests
import web3
from web3 import Web3


MAINNET_ACCESS_URL = config('MAINNET_ACCESS_URL')

w3 = Web3(Web3.HTTPProvider(f"{MAINNET_ACCESS_URL}"))

ETHERSCAN_KEY = config("ETHERSCAN_KEY")

address = Web3.toChecksumAddress("0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5")

r = requests.get(f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={ETHERSCAN_KEY}').json()
path = os.path.join('abi','abi.json')
with open(path) as f:
    abi = f.read()

tellor_core = w3.eth.contract(address=address, abi=abi)