import json
from web3 import Web3
import time
import requests
from utils import (
    init_rosefraxpool, 
    init_garden,
    init_nearpad_dex_router,
    init_rosepool,
    init_nearpadpool,
    init_token,
    get_apr,
    TEN18,
    TEN18_INV,
    TEN6,
)

GARDEN_WBTC = Web3.toChecksumAddress("0x6bA5B45149996597d96e6dB19E4E1eFA81a6df97")
GARDEN_NEAR = Web3.toChecksumAddress("0x64C922E3824ab40cbbEdd6C8092d148C283d3D3D")
GARDEN_USDC = Web3.toChecksumAddress("0xfbAF3eBF228eB712b1267285787e51aDd70086bB")
GARDEN_USDT = Web3.toChecksumAddress("0x0F44fCD177098Cb2B063B50f6C62e4F1E1f9d596")
GARDEN_WETH = Web3.toChecksumAddress("0x084355FDd5fcfd55d60C5B8626756a6906576f13")
GARDEN_UST = Web3.toChecksumAddress("0xe8F7F08D50e12145Cb722cfF861e6A9b43EADBA1")

gardens = {
    "WBTC": {
        "address": GARDEN_WBTC,
        "decimals": 8,
        "coingecko": "wrapped-bitcoin"
    },
    "NEAR": {
        "address": GARDEN_NEAR,
        "decimals": 24,
        "coingecko": "near"
    },
    "USDC": {
        "address": GARDEN_USDC,
        "decimals": 6,
        "coingecko": "usd-coin"
    },
    "USDT": {
        "address": GARDEN_USDT,
        "decimals": 6,
        "coingecko": "tether"
    },
    "WETH": {
        "address": GARDEN_WETH,
        "decimals": 18,
        "coingecko": "ethereum"
    },
    "UST": {
        "address": GARDEN_UST,
        "decimals": 18,
        "coingecko": "terrausd"
    },
}

ROSE = Web3.toChecksumAddress("0xdcD6D4e2B3e1D1E1E6Fa8C21C8A323DcbecfF970")
STROSE = Web3.toChecksumAddress("0xe23d2289FBca7De725DC21a13fC096787A85e16F")
PAD = Web3.toChecksumAddress("0x885f8CF6E45bdd3fdcDc644efdcd0AC93880c781")
FRAX = Web3.toChecksumAddress("0xda2585430fef327ad8ee44af8f1f989a2a91a3d2")
DAI = Web3.toChecksumAddress("0xe3520349F477A5F6EB06107066048508498A291b")
USDC = Web3.toChecksumAddress("0xB12BFcA5A55806AaF64E99521918A4bf0fC40802")
USDT = Web3.toChecksumAddress("0x4988a896b1227218e4A686fdE5EabdcAbd91571f")

pools = {
    "Stables Pool": {
        "pool_address": "0xc90db0d8713414d78523436dc347419164544a3f",
        "contract_name": "RoseStablesPool"
    },
    "Frax Pool": {
        "pool_address": "0xa34315f1ef49392387dd143f4578083a9bd33e94",
        "contract_name": "FraxPool"
    },
    "UST Pool": {
        "pool_address": "0x8fe44f5cce02d5be44e3446bbc2e8132958d22b8",
        "contract_name": "USTPool"
    },
    "BUSD Pool": {
        "pool_address": "0xd6cb7bb7d63f636d1ca72a1d3ed6f7f67678068a",
        "contract_name": "BUSDPool"
    },
    "MAI Pool": {
        "pool_address": "0x65a761136815b45a9d78d9781d22d47247b49d23",
        "contract_name": "MAIPool"
    },
    "RUSD Pool": {
        "pool_address": "0x79b0a67a4045a7a8dc04b17456f4fe15339cba34",
        "contract_name": "RUSDPool"
    }
}

lpAddresses = {
    "Stables Farm": {
        "deposited_token_address": "0xfF79D5bff48e1C01b722560D6ffDfCe9FC883587",
        "farm_address": "0x52CACa9a2D52b27b28767d3649565774A3B991f3",
        "pool_address": pools["Stables Pool"]["pool_address"],
        "this_months_rewards": 547601.00
    },
    "Frax Farm": {
        "deposited_token_address": "0x4463A118A2fB34640ff8eF7Fe1B3abAcd4aC9fB7",
        "farm_address": "0xB9D873cDc15e462f5414CCdFe618a679a47831b4",
        "pool_address": pools["Frax Pool"]["pool_address"],
        "this_months_rewards": 127349.00
    },
    "UST Farm": {
        "deposited_token_address": "0x94A7644E4D9CA0e685226254f88eAdc957D3c263",
        "farm_address": "0x56DE5E2c25828040330CEF45258F3FFBc090777C",
        "pool_address": pools["UST Pool"]["pool_address"],
        "this_months_rewards": 0.00
    },
    "ROSE/FRAX PLP Farm": {
        "deposited_token_address": "0xeD4C231b98b474f7cAeCAdD2736e5ebC642ad707",
        "farm_address": "0x1B10bFCd6192edC573ced7Db7c7e403c7FAb8068",
        "this_months_rewards": 0.00
    },
    "ROSE/PAD PLP Farm": {
        "deposited_token_address": "0xC6C3cc84EabD4643C382C988fA2830657fc70a6B",
        "farm_address": "0x9b2aE7d53099Ec64e2f6df3B4151FFCf7205f788",
        "this_months_rewards": 167162.00
    },
    "BUSD Farm" : {
        "deposited_token_address": "0x158f57CF9A4DBFCD1Bc521161d86AeCcFC5aF3Bc",
        "farm_address": "0x18A6115150A060F22Bacf62628169ee9b231368f",
        "this_months_rewards": 63675.00,
        "pool_address": pools["BUSD Pool"]["pool_address"]
    },
    "MAI Farm" : {
        "deposited_token_address": "0xA7ae42224Bf48eCeFc5f838C230EE339E5fd8e62",
        "farm_address": "0x226991aADeEfDe03bF557eF067da95fc613aBfFc",
        "this_months_rewards": 25470.00,
        "pool_address": pools["MAI Pool"]["pool_address"]
    },
    "RUSD Farm" : {
        "deposited_token_address": "0x56f87a0cB4713eB513BAf57D5E81750433F5fcB9",
        "farm_address": "0x9286d58C1c8d434Be809221923Cf4575f7A4d058",
        "this_months_rewards": 771894.00,
        "pool_address": pools["RUSD Pool"]["pool_address"]
    }
}

data = []
rose_data = []
pool_data = []
w3 = Web3(Web3.HTTPProvider("https://mainnet.aurora.dev/"))

def get_pad_token_price(first, div0=TEN18):
    div0_inv = 1. / div0
    pad_token_out = (nearpad_dex_router.functions.getAmountsOut(TEN18, [PAD, first]).call())[1] * div0_inv
    token_pad_in = (nearpad_dex_router.functions.getAmountsIn(TEN18, [first, PAD]).call())[0] * div0_inv
    token_pad_out = (nearpad_dex_router.functions.getAmountsOut(div0, [first, PAD]).call())[1] * TEN18_INV
    pad_token_in = (nearpad_dex_router.functions.getAmountsIn(div0, [PAD, first]).call())[0] * TEN18_INV
    return (pad_token_out + token_pad_in + 1. / token_pad_out + 1. / pad_token_in) * 0.25

# get price of ROSE 
nearpad_dex_router = init_nearpad_dex_router(w3)

# PAD/ROSE
pad_rose_price = get_pad_token_price(ROSE)
print('PAD/ROSE: {:.5g}'.format(pad_rose_price))

# ROSE/FRAX
rose_frax_price = (nearpad_dex_router.functions.getAmountsOut(TEN18, [ROSE, FRAX]).call())[1]
rose_frax_price = float(rose_frax_price) * TEN18_INV
print("ROSE/FRAX Price: {:.5g}".format(rose_frax_price))

# ROSE/DAI
pad_dai_price = get_pad_token_price(DAI, div0=TEN18)
rose_dai_price = pad_dai_price / pad_rose_price
print("ROSE/DAI Price: {:.5g}".format(rose_dai_price))

# ROSE/USDC
pad_usdc_price = get_pad_token_price(USDC, div0=TEN6)
rose_usdc_price = pad_usdc_price / pad_rose_price
print("ROSE/USDC Price: {:.5g}".format(rose_usdc_price))

# ROSE/USDT
pad_usdt_price = get_pad_token_price(USDT, div0=TEN6)
rose_usdt_price = pad_usdt_price / pad_rose_price
print("ROSE/USDT Price: {:.5g}".format(rose_usdt_price))

# ROSE price
rose_price = (rose_frax_price + rose_dai_price + rose_usdc_price + rose_usdt_price) * 0.25
# roseprice = rose_frax_price # temp
print("ROSE (averaged) price: {:.5g}".format(rose_price))

# get tvl of stROSE
rose_contract = init_token(w3, ROSE)
strose_rose_balance_c = rose_contract.functions.balanceOf(STROSE).call()
strose_rose_balance = float(strose_rose_balance_c) * TEN18_INV
strose_tvl_f = strose_rose_balance * rose_price
strose_tvl = round(strose_tvl_f) * TEN18

# get price of stRose
strose_contract = init_token(w3, STROSE)
strose_total_supply = strose_contract.functions.totalSupply().call()
strose_total_supply = float(strose_total_supply) * TEN18_INV
print("stRose total supply: ", strose_total_supply)
strose_rose_ratio = strose_rose_balance / strose_total_supply
stroseprice = rose_price * strose_rose_ratio

# fetch volume from subgraph for each pool
totalDailyVolume = 0
# totalWeeklyVolume = 0
for poolName, poolPayload in pools.items():
    query = "{" + poolPayload["contract_name"] + ": pools(where: {id: \"" + poolPayload["pool_address"] + """\"}){
        dailyVolumes(
            first: 2
            orderBy: timestamp,
            orderDirection: desc
        ) {
            volume
            timestamp
        }
        weeklyVolumes(
            first: 2
            orderBy: timestamp,
            orderDirection: desc
        ) {
            volume
            timestamp
        }
      }}"""
    try:
        result = requests.post(
            "https://api.thegraph.com/subgraphs/name/roseonaurora/rose",
            json={"query": query}
        )
        result = json.loads(result.text)['data'][poolPayload["contract_name"]][0]
        dailyVolume = result['dailyVolumes'][1]['volume'] # last day
        # weeklyVolume = result['weeklyVolumes'][1]['volume'] # last week

        totalDailyVolume += float(dailyVolume)
        # totalWeeklyVolume += float(weeklyVolume)

        pool_data.append({
            "pool_name": poolName,
            "daily_volume": dailyVolume,
            # "weekly_volume": weeklyVolume
        })
    except Exception as e:
        print("error: ", e)
        continue

with open('pools.json', 'w', encoding='utf-8') as f:
    json.dump(pool_data, f, ensure_ascii=False, indent=4)

# calculate stROSE APR
strose_apr_float = (((totalDailyVolume * 0.0004 * 0.63) / strose_total_supply) * 365) / (strose_rose_ratio * rose_price)
strose_apr = str("{:0.1f}%".format(strose_apr_float * 100))

rose_data.append({
    "price_of_rose": str(rose_price),
    "price_of_strose": str(stroseprice),
    "strose_rose_ratio": str(strose_rose_ratio),
    "strose_tvl": str(strose_tvl),
    "strose_apr": str(strose_apr),
    "total_rose_staked": str(strose_rose_balance_c),
    "total_daily_volume": str(totalDailyVolume),
    # "total_weekly_volume": str(totalWeeklyVolume)
})

with open('rose.json', 'w', encoding='utf-8') as f:
    json.dump(rose_data, f, ensure_ascii=False, indent=4)

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
        farmBalanceStr = str(farmBalance)
        print(farmName, "deposits balance:", float(farmBalanceStr[:len(farmBalanceStr)-18]))
    except:
        print("Error fetching farm balance")
        pass

    # calculate virtual price and TVL
    if farmName == "Stables Farm" or farmName == "Frax Farm" or farmName == "UST Farm" or farmName == "BUSD Farm" or farmName == "MAI Farm" or farmName == "RUSD Farm":
        virtualPrice = rose_price
        # assume LP token = $1
        virtualPrice = 1.0
        farmTvl = farmBalance
    elif farmName == "ROSE/FRAX PLP Farm":
        farmBalance = farmBalance * TEN18_INV
        try:
            rosefraxpool = init_rosefraxpool(w3)
            pool_reserves = rosefraxpool.functions.getReserves().call()
            frax_reserves = round(float(pool_reserves[0]) * TEN18_INV, 0)
            # assume pool is balanced and multiply FRAX reserve by two
            virtualPrice = float(frax_reserves*2) / float(farmBalance)
            farmTvl = int(round(farmBalance * virtualPrice))
            farmTvl = farmTvl * 10**18
        except:
            print("Error getting farm balance for", farmName)
    elif farmName == "ROSE/PAD PLP Farm":
        farmBalance = farmBalance / 10**18
        pool = init_nearpadpool(w3, payload["deposited_token_address"])
        try:
            reserves = pool.functions.getReserves().call()
            reservesRose = float(reserves[1])
            reservesRose = round(reservesRose * TEN18_INV, 0)
            # assupme pool is balanced and multiply ROSE usd value reserves by two
            virtualPrice = (reservesRose * rose_price) * 2 / farmBalance
            farmTvl = int(round(farmBalance * virtualPrice))
            farmTvl = farmTvl * TEN18
        except:
            print("Error getting farm balance for", farmName)

    print(farmName, "deposit token virtual price:", virtualPrice)
    
    # format TVL to float for apr calculation
    farmTvl = str(farmTvl)
    try:
        farmTvlFloat = float(farmTvl[:len(farmTvl)-18])
    except:
        print("Error converting farm tvl to float")
        farmTvlFloat = 0.0
    print(farmName, "deposits TVL:", farmTvlFloat)
    
    # calculate APR
    apr_float = get_apr(rose_price, rewardsPerSecond, farmTvlFloat)

    if farmTvlFloat == 0:
        apr = "∞%"
    else:
        apr = str("{:0.0f}%".format(apr_float))

    # calculate apr for second rewards token, if any
    second_rewards_token = payload.get("second_rewards_token")
    if second_rewards_token is not None:
        try:
            result = requests.get("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + payload["second_rewards_token"])
        except:
            print("Error fetching second rewards token price")
        second_rewards_per_second = payload["second_this_months_rewards"] / 30 / 24 / 60 / 60
        second_token_price = result.json()[second_rewards_token]["usd"]
        second_apr_float = get_apr(second_token_price, second_rewards_per_second, farmTvlFloat)
        second_apr = str("{:0.0f}%".format(second_apr_float))
        second_rewards_token = payload["second_rewards_token_symbol"]
        second_rewards_token_address = payload["second_rewards_token_address"]
    else:
        second_apr = ""
        second_rewards_token = ""
        second_token_price = ""
        second_rewards_per_second = ""
        second_rewards_token_address = ""

    data.append({
        "name": farmName,
        "deposited_token_address": payload["deposited_token_address"],
        "farm_address": payload["farm_address"],
        "farm_tvl": str(farmTvl),
        "deposited_token_price": str(virtualPrice),
        "rewards_per_second": str(rewardsPerSecond),
        "apr": apr,
        "second_rewards_token": second_rewards_token,
        "second_apr": second_apr,
        "second_token_price": str(second_token_price),
        "second_rewards_per_second": str(second_rewards_per_second),
        "second_rewards_token_address": second_rewards_token_address
    })

gardensData = []
totalCollateralValue = 0
totalBorrowed = 0
for garden_name, payload in gardens.items():
    print(garden_name, "garden stats:")
    # instantiate contract
    garden = init_garden(w3, payload["address"])

    # get token value
    value = 0
    try:
        result = requests.get("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + payload["coingecko"])
        value = result.json()[payload["coingecko"]]["usd"]
    except:
        print("Error fetching garden token price")
    print("token value: $", value)

    # get total collateral and collateral value
    collateral = garden.functions.totalCollateralShare().call()
    collateral = float(collateral) * 1. / 10**(payload["decimals"])
    print("collateral:", collateral, garden_name)
    collateralValue = collateral * value
    print("collateral value: $", collateralValue)
    totalCollateralValue += collateralValue

    # get borrowed
    borrowed = garden.functions.totalBorrow().call()[0]
    borrowed = float(borrowed) * TEN18_INV
    print("borrowed:", borrowed, "RUSD")
    totalBorrowed += borrowed

    gardensData.append({
        "garden": garden_name,
        "token_value": value,
        "collateral": collateral,
        "collateral_value": collateralValue,
        "borrowed": borrowed
    })

print("total borrowed:", totalBorrowed, "RUSD")
print("total collateral: $", totalCollateralValue)
totalCollateralRatio = totalCollateralValue / totalBorrowed
print("total collateralization ratio:", (totalCollateralRatio * 100), "%")
gardensData.append({
    "total_borrowed": totalBorrowed,
    "total_collateral_value": totalCollateralValue,
    "total_collateralization_ratio": totalCollateralRatio
})

with open('gardens.json', 'w', encoding='utf-8') as f:
    json.dump(gardensData, f, ensure_ascii=False, indent=4)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Done")
