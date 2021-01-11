import argparse
import json
import os
import time

from decouple import config
import pandas as pd
import requests
from tqdm import tqdm
import web3
from web3 import Web3

class Events:

    def __init__(self, start_block = int(config('START_BLOCK')), api_key=config('MAINNET_ACCESS_URL')):
        self.w3 = Web3(Web3.HTTPProvider(f"{api_key}"))
        self.start_block = start_block
        self.last_block = self.w3.eth.blockNumber
        self.api_key = api_key
        path = os.path.join('abi', 'abi.json')
        with open(path) as f:
            abi = f.read()
        self.address = Web3.toChecksumAddress("0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5")
        self.tellor_contract = self.w3.eth.contract(address=self.address, abi=abi)

    def get_transfers(self):
        start_block = self.start_block
        last_block = self.last_block
        entries = []

        for i in tqdm(range(start_block, last_block, 2000)):

            transfers = self.tellor_contract.events.Transfer.createFilter(fromBlock=i, toBlock=i + 2000)
            new_events = transfers.get_all_entries()
            for j in new_events:
                _from = j['args']['_from']
                _to = j['args']['_to']
                _value = j['args']['_value']
                tx_hash = j['transactionHash'].hex()
                address = j['address']
                eth_block_number = j['blockNumber']
                entry = dict(_from=_from, _to=_to,
                            _value=_value, tx_hash=tx_hash,
                            address=address, eth_block_number=eth_block_number
                            )
                entries.append(entry)
            
        df = pd.DataFrame(entries)
        
        gas_prices = []
        for i in df['tx_hash']:
            try:
                gas_price = self.w3.eth.getTransaction(i).gasPrice
                gas_prices.append(gas_price)
            except Exception as e:
                time.sleep(86460)
        
        df['gas_price'] = gas_prices

        eth_block_timestamps = []
        for i in df['eth_block_number']:
            try:
                block_timestamp = self.w3.eth.getBlock(i).timestamp
                eth_block_timestamps.append(block_timestamp)
            except Exception as e:
                time.sleep(86460)
        
        print(df.head())
        #Path to csv
        path = os.path.join('data', 'transfers.csv')
        #If csv already exists
        if os.path.isfile(path):
            # old_df = pd.read_csv(path)
            # df = old_df.append(df, ignore_index=False)
            df.to_csv(path, header = False, mode='a')
        #If csv need to be created (first query)
        else:
            df.to_csv(path, index=False)
    def set_start_block(self):
        self.start_block = self.last_block
        with open('.env', 'r') as reader:
            for line in reader.readlines():
                try:
                    key, value = line.split('=')
                    if key == 'START_BLOCK':
                        with open('.env', 'w') as writer:
                            writer.replace(value, self.start_block)
                except Exception as e:
                    e.with_traceback()

if __name__ == '__main__':
    print(os.getcwd())
    breakpoint()
    ev = Events()
    ev.get_transfers()
    ev.set_start_block()