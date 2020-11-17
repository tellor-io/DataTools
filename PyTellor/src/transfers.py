from itertools import chain

import pandas as pd
import requests

from keys import *

#paramaters for query
start_block = 8000000
last_block = w3.eth.blockNumber
entries = []
# transfers = tellor_core.events.Transfer.createFilter(fromBlock=start_block)

# events = transfers.get_all_entries()
for i in range(start_block, last_block, 2000):

    transfers = tellor_core.events.Transfer.createFilter(fromBlock=i, toBlock=i + 2000)
    new_events = transfers.get_all_entries()
    entries.append(new_events)
    print(len(new_events))
    
print(len(entries))

# print(events[:5])