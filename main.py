import time
from trader import Trader
from exchange import get_full_balance              

# put whichever coins you want to trade on in a list, and create a trader class for each
# tick every minute
if __name__ == "__main__":
    get_full_balance()
    coins = ['LINK','BNB','ETH','BTC']
    traders = list()

    for coin in coins:
        traders.append(Trader(coin))

    while True:
        for trader in traders:
            trader.tick()
            print('==========================')
        time.sleep(60)
     
