import json
from web3 import Web3
from utils import (
    init_rosefraxpool, 
    init_rosepool,
    init_nearpadpool,
    init_token,
    getAPR,
)

lpAddresses = {
    "Stables Farm": {
        "deposited_token_address": "0xfF79D5bff48e1C01b722560D6ffDfCe9FC883587",
        "farm_address": "0x52CACa9a2D52b27b28767d3649565774A3B991f3",
        "pool_address": "0xc90dB0d8713414d78523436dC347419164544A3f",
        "this_months_rewards": 450275.00
    },
    # "Frax Farm": {
    #     "deposited_token_address": "0xbB5279353d88A25F099A334Ba49CDCb1CF4b5A7c",
    #     "farm_address": "0x7b359Af630a195C05Ac625D261aEe09a69aF7744",
    #     "pool_address": "0xd812cc1fc1e0a56560796C746B1247e2bd4F31f2",
    #     "this_months_rewards": 1000.00
    # },
    # "stRose Farm": {
    #     "deposited_token_address": "0x7Ba8C17010a48283D38a4bd5f87EfEB5594c92f8",
    #     "farm_address": "0x247c9DA96BfC4720580ee84E01566D79a8c901ca",
    #     "pool_address": "0x36685AfD221622942Df61979d72a0064a17EF291",
    #     "this_months_rewards": 1000.00
    # },
    "ROSE/FRAX NLP Farm": {
        "deposited_token_address": "0xeD4C231b98b474f7cAeCAdD2736e5ebC642ad707",
        "farm_address": "0x1B10bFCd6192edC573ced7Db7c7e403c7FAb8068",
        "this_months_rewards": 225137.00
    },
    "ROSE/PAD NLP Farm": {
        "deposited_token_address": "0xC6C3cc84EabD4643C382C988fA2830657fc70a6B",
        "farm_address": "0x9b2aE7d53099Ec64e2f6df3B4151FFCf7205f788",
        "this_months_rewards": 525321.00
    },
}
data = []
rose_data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

# get price of ROSE against FRAX
rosefraxpool = init_rosefraxpool(w3)
roseprice = 0
pool_reserves = rosefraxpool.functions.getReserves().call()
frax_reserves = round(float(pool_reserves[0]) / 10**18, 0)
rose_reserves = round(float(pool_reserves[1]) / 10**18, 0)
print("ROSE/FRAX reserves: ", frax_reserves, rose_reserves)
roseprice = frax_reserves / rose_reserves
print("ROSE/FRAX price: ", roseprice)

rose_data.append({
    "price_of_rose": str(roseprice)
})

# fetch apr for each farm
for farmName, payload in lpAddresses.items():
    print("Fetching APR for", farmName)

    # get rewards per second for this farm
    rewardsPerSecond = payload["this_months_rewards"] / 30 / 24 / 60 / 60

    farmTvl = 0
    deposited_token = init_token(w3, payload["deposited_token_address"])
    virtualPrice = 0

    # fetch farm balance
    farmBalance = 0
    try:
        farmBalance = deposited_token.functions.balanceOf(payload["farm_address"]).call()
    except:
        print("Error fetching farm balance")
        continue

    if farmName == "Stables Farm":
        # assume LP token = $1 for stables farm
        virtualPrice = 1.0
        farmTvl = farmBalance
    elif farmName == "Frax Farm":
        # assume LP token = $1 for frax farm
        virtualPrice = 1.0
        farmTvl = farmBalance
    elif farmName == "ROSE/FRAX NLP Farm":
        farmBalance = farmBalance / 10**18
        try:
            # assume pool is balanced and multiply FRAX reserve by two
            print("FRAX reserves: ", frax_reserves)
            virtualPrice = frax_reserves*2 / farmBalance
            farmTvl = int(round(farmBalance * virtualPrice))
            farmTvl = farmTvl * 10**18
        except:
            print("Error getting farm balance for", farmName)
    elif farmName == "ROSE/PAD NLP Farm":
        # calculate TVL
        farmBalance = farmBalance / 10**18
        pool = init_nearpadpool(w3, payload["deposited_token_address"])
        try:
            reserves = pool.functions.getReserves().call()
            reservesRose = float(reserves[1])
            print("PAD reserves: ", reservesRose)
            reservesRose = round(reservesRose / 10**18, 0)
            # assupme pool is balanced and multiply ROSE usd value reserves by two
            virtualPrice = (reservesRose*roseprice)*2 / farmBalance
            farmTvl = int(round(farmBalance * virtualPrice))
            farmTvl = farmTvl * 10**18
        except:
            print("Error getting farm balance for", farmName)
    
    # print("roseprice:", roseprice)
    # rewardsPerSecond = round(rewardsPerSecond, 3)
    # print("rewardsPerSecond:", rewardsPerSecond)
    print("farmTvl:", farmTvl)
    farmTvl = str(farmTvl)
    farmTvlFloat = float(farmTvl[:len(farmTvl)-18])
    print("farmTvlFloat:", farmTvlFloat)
    apr_float = getAPR(roseprice, rewardsPerSecond, farmTvlFloat)
    # apr_float = 0
    print("APR float:", apr_float)
    apr = str("{:0.1f}".format(apr_float)) + "%"
    # apr = str(int(round(apr_float))) + "%"

    data.append({
        "name": farmName,
        "deposited_token_address": payload["deposited_token_address"],
        "farm_address": payload["farm_address"],
        "farm_tvl": str(farmTvl),
        "deposited_token_price": str(virtualPrice),
        "rewards_per_second": str(rewardsPerSecond),
        "apr": apr, 
    })

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open('rose.json', 'w', encoding='utf-8') as f:
    json.dump(rose_data, f, ensure_ascii=False, indent=4)
