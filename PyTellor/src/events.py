import argparse
import json
import os
import time
import sys

from decouple import config
import pandas as pd
import requests
from tqdm import tqdm
import web3
from web3 import Web3

class Events:

    def __init__(self, last_block, start_block = int(config('START_BLOCK')), api_key=config('MAINNET_ACCESS_URL')):
        self.w3 = Web3(Web3.HTTPProvider(f"{api_key}", request_kwargs={'timeout':60}))
        self.start_block = start_block
        self.last_block = last_block
        self.api_key = api_key
        path = os.path.join('abi', 'abi.json')
        with open(path) as f:
            abi = f.read()
        self.address = Web3.toChecksumAddress("0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0")
        self.tellor_contract = self.w3.eth.contract(address=self.address, abi=abi)
        print(self.tellor_contract.all_functions())

    def get_transfers(self, output_file):
        start_block = self.start_block
        last_block = self.last_block
        df = pd.DataFrame(columns=['_from', '_to', '_value', '_tx_hash', 'address', 'eth_block_number', 'eth_block_timestamp'])
        #Iterate through chunks
        for i in tqdm(range(start_block, last_block, 2000)):
                #Search for transfer events in 5000-block intervals
                transfers = self.tellor_contract.events.Transfer.createFilter(fromBlock=i, toBlock=i+2000)
                #Pull transfer events into list -- these are AttributeDicts
                new_events = transfers.get_all_entries()
                #Iterate through List of AttributeDicts
                for j in new_events:
                    #The desired values
                    _from = j['args']['_from']
                    _to = j['args']['_to']
                    _value = j['args']['_value']
                    tx_hash = j['transactionHash'].hex()
                    address = j['address']
                    eth_block_number = j['blockNumber']
                    # gas_price = self.w3.eth.getTransaction(tx_hash).gasPrice
                    eth_block_timestamp = self.w3.eth.getBlock(eth_block_number).timestamp
                    #Make new dictionary from desired values
                    entry = dict(_from=_from, _to=_to,
                                _value=_value, tx_hash=tx_hash,
                                address=address, eth_block_number=eth_block_number,
                                # gas_price=gas_price, 
                                eth_block_timestamp=eth_block_timestamp
                                )
                    #Append refactored event dict to entries List
                    df.append(entry)
                    #Deleting loop variables to prevent running out of RAM on node machine
                    del _from, _to, _value, tx_hash, address, eth_block_number, entry, eth_block_timestamp
                    # del gas_price
                del transfers, new_events
            
                
        # df = pd.DataFrame(entries)
        #Path to csv
        path = os.path.join('data', output_file)
        #If csv already exists
        if os.path.isfile(path):
            df.to_csv(path, header = False, mode='a')
        #If csv need to be created (first query)
        else:
            df.to_csv(path, index=False)
    def set_start_block(self):
        '''
        Adjusts start_block env variable in .env text file.
        Meant to be called after get_transfers() so that future
        queries (future calls of get_transfers()) don't read the same block twice.
        '''

        #The new start block is the last block read
        self.start_block = self.last_block
        #Rewrite .env file with new start block value
        with open('.env', 'r') as reader:
            for line in reader.readlines():
                try:
                    key, value = line.split('=')
                    if key == 'START_BLOCK':
                        line = line.replace(value, str(self.start_block))
                        with open('.env', 'w') as writer:
                            writer.write(line)
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    ev = Events(start_block=8102967, last_block=8200000)
    ev.get_transfers('test1.csv')
    # ev.set_start_block()