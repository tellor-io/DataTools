import os
import pandas as pd
import requests
from tqdm import tqdm

from keys import *

#parameters for query
start_block = 8000000
last_block = w3.eth.blockNumber
entries = []

for i in tqdm(range(last_block-2000, last_block, 2000)):

    filt = tellor_core.events.NewValue.createFilter(fromBlock=i, toBlock=i+2000)
    events = filt.get_all_entries()
    for j in events:
        
