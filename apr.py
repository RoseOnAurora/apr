import json
from web3 import Web3
from utils import (
    init_rosefraxpool, 
    init_token,
    getAPR,
)

lpAddresses = {
    "Stables Farm": {
        "deposited_token_address": "0xfF79D5bff48e1C01b722560D6ffDfCe9FC883587",
        "farm_address": "0x52CACa9a2D52b27b28767d3649565774A3B991f3",
        "this_months_rewards": 1000.00
    }
}
data = []
rose_data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

# get price of ROSE against FRAX
rosefraxpool = init_rosefraxpool(w3)
roseprice = 0
try:
    roseprice = rosefraxpool.functions.price0CumulativeLast().call()
except:
    print("Error getting price of ROSE against FRAX")

rose_data.append({"price_of_rose": str(roseprice)})

# fetch apr for each farm
for farmName, payload in lpAddresses.items():
    print("Fetching APR for", farmName)

    # get rewards per second for this farm
    rewardsPerSecond = payload["this_months_rewards"] / 30 / 24 / 60 / 60

    farmTvl = 0
    if farmName == "Stables Farm":
        deposited_token = init_token(w3, payload["deposited_token_address"])
        # assume LP token = $1 for stables farm
        farmTvl = deposited_token.functions.balanceOf(payload["farm_address"]).call()

    apr_float = getAPR(roseprice, rewardsPerSecond, farmTvl)
    apr = str("{:0.1f}".format(apr_float)) + "%"

    data.append({
        "farm": farmName,
        "deposited_token_address": payload["deposited_token_address"],
        "farm_tvl": str(farmTvl),
        "apr": apr,
    }) 

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open('rose.json', 'w', encoding='utf-8') as f:
    json.dump(rose_data, f, ensure_ascii=False, indent=4)
