from itertools import chain
import os
import pandas as pd
import requests
from tqdm import tqdm

from keys import *

#paramaters for query
start_block = 8000000
last_block = w3.eth.blockNumber
entries = []


# events = transfers.get_all_entries()
for i in tqdm(range(start_block, last_block, 2000)):

    transfers = tellor_core.events.Transfer.createFilter(fromBlock=i, toBlock=i + 2000)
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

df['gas_price'] = df['tx_hash'].apply(lambda x: w3.eth.getTransaction(x).gasPrice)
df['block_timestamp'] = df['eth_block_number'].apply(lambda x: w3.eth.getBlock(x).timestamp)

print(df.head())

path = os.path.join('data', 'transfers.csv')
df.to_csv(path, index=False)