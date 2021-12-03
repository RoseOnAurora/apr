import json

# for fetching USD price of Rose
NEARPAD_ROSE_FRAX_POOL = "0xeD4C231b98b474f7cAeCAdD2736e5ebC642ad707"

def init_rosefraxpool(w3):
    with open('abis/NearPadPool.json') as json_file:
        return w3.eth.contract(
            address=NEARPAD_ROSE_FRAX_POOL,
            abi=json.load(json_file)
        )

def init_token(w3, tokenAddress):
    with open('abis/erc20.json') as json_file:
        return w3.eth.contract(
            address=tokenAddress,
            abi=json.load(json_file)
        )

def getAPR(priceInUsd, totalRewardRate, totalStakedInUsd):
    if totalStakedInUsd == 0:
        return 0
    else:
        totalYearlyRewards = totalRewardRate * 3600 * 24 * 365
        return totalYearlyRewards*100*10**6/(totalStakedInUsd*priceInUsd)
