import json

# for fetching USD price of Rose
NEARPAD_ROSE_FRAX_POOL = "0xeD4C231b98b474f7cAeCAdD2736e5ebC642ad707"
NEARPAD_DEX_ROUTER = "0xBaE0d7DFcd03C90EBCe003C58332c1346A72836A"

def init_rosefraxpool(w3):
    with open('abis/NearPadPool.json') as json_file:
        return w3.eth.contract(
            address=NEARPAD_ROSE_FRAX_POOL,
            abi=json.load(json_file)
        )

def init_nearpad_dex_router(w3):
    with open('abis/NearPadDEXRouter.json') as json_file:
        return w3.eth.contract(
            address=NEARPAD_DEX_ROUTER,
            abi=json.load(json_file)
        )

def init_nearpadpool(w3, poolAddress):
    with open('abis/NearPadPool.json') as json_file:
        return w3.eth.contract(
            address=poolAddress,
            abi=json.load(json_file)
        )

def init_token(w3, tokenAddress):
    with open('abis/erc20.json') as json_file:
        return w3.eth.contract(
            address=tokenAddress,
            abi=json.load(json_file)
        )

def init_rosepool(w3, poolAddress):
    with open('abis/RosePool.json') as json_file:
        return w3.eth.contract(
            address=poolAddress,
            abi=json.load(json_file)
        )

def getAPR(rosePriceInUsd, roseRewardRate, totalStakedInUsd):
    if totalStakedInUsd == 0:
        return 0
    else:
        totalYearlyRewards = roseRewardRate * 3600 * 24 * 365
        totalYearlyRewardsUsd = totalYearlyRewards * rosePriceInUsd

        futureValue = totalStakedInUsd + totalYearlyRewardsUsd

        return (float(totalYearlyRewardsUsd) / float(totalStakedInUsd)) * 100

