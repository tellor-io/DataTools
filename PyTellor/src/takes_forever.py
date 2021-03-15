import csv
import os
import time

from decouple import config
import pandas as pd
from tqdm import tqdm
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(config("MAINNET_ACCESS_URL"), request_kwargs={'timeout':60}))
with open('transfers.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        #skip over column names
        if line_count == 0:
            

gas_prices = []
for i in tqdm(df['tx_hash']):
    gas_price = w3.eth.getTransaction(i).gasPrice
    gas_prices.append(gas_price)

    del gas_price
df['gas_price'] = gas_prices

eth_block_timestamps = []
for i in tqdm(df['eth_block_number']):
    block_timestamp = w3.eth.getBlock(i).timestamp
    eth_block_timestamps.append(block_timestamp)

    del block_timestamp
df['eth_block_timestamp'] = eth_block_timestamps
