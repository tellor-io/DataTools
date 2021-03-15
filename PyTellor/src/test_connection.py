from decouple import config
from web3 import Web3

MAINNET_URL = config('MAINNET_ACCESS_URL')

w3 = Web3(Web3.HTTPProvider(MAINNET_URL))

print(w3.isConnected())
