import pandas as pd
import requests

from keys import *

#variables for request
vote_init_block = 11074853
end_block = 11111896
topic0 = "0x911ef2e98570b1d96c0e8ef81107a33d5b8e844aeb8f9710f9bc76c3b3fef40e"

r = requests.get(f'https://api.etherscan.io/api?module=logs&action=getLogs&address={address}&fromBlock={vote_init_block}&toBlock={end_block}&topic0={topic0}&apikey={ETHERSCAN_KEY}').json()

##Loop through voters query to find the balances of the voters

counter = 0
addresses = []
balances = []

for i in r['result']:
    #convert and save voter addresses
    voter_address = "0x" + i['topics'][2][-40:]
    voter_address_checksum = Web3.toChecksumAddress(voter_address)
    addresses.append(voter_address_checksum)
    #convert to decimal from hexa
    balance = tellor_core.functions.balanceOfAt(voter_address_checksum, vote_init_block).call()
    #convert from wei to trb
    balances.append(balance/(1E18))

#Create dataframe with address and balance
#Will be merged with Voting Position
df_balances = pd.DataFrame({"Address" : addresses, "Balance" : balances})

#Streaming voter events
tellor_filter = tellor_core.events.Voted.createFilter(fromBlock=vote_init_block, toBlock=end_block, topics=[topic0])

votes = tellor_filter.get_all_entries()

##Loop through voting events to find position on TIP

positions = [voter['args']['_position'] for voter in votes]
addresses = [voter['args']['_voter'] for voter in votes]

df_votes = pd.DataFrame({"Address": addresses, "Vote": positions})

#merge balances and voting positions on addresses
df = pd.merge(df_balances, df_votes, on='Address')

#create DataFrame for addresses and voting position to be merged to main DataFrame
df = df.sort_values(by=["Balance"], ascending=True)
df.to_csv('votes.csv', index=False)