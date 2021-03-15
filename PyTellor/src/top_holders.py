'''
Script that scrapes the Ethereum blockchain and outputs the top TRB holders in a graph and a csv.
'''

import pandas as pd
import seaborn as sns
import web3
from web3 import Web3