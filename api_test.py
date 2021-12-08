from nomics import Nomics
import pandas as pd
import json




key = "266dbf914fd18fad344fcf6e0937362695777573"



nomics = Nomics(key)

date_1 = '2020-10-12 07:20:50.52Z'
date_2 = '2021-10-12 07:20:50.52'

markets = nomics.Currencies.get_currencies('ETH')
#meta = nomics.Currencies.get_metadata('LINK')

#df = pd.read_json(markets)
#print(markets)
df = pd.DataFrame(markets[0])
print(df['1d']['volume'])

#print(df)
#print(markets)
#df = pd.read_json(markets)

#with open('data.txt', 'w') as f:
    #json.dump(markets, f)
