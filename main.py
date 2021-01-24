import time
from trader import Trader
from exchange import get_full_balance              

# put whichever coins you want to trade on in a list, and create a trader class for each
# tick every minute
if __name__ == "__main__":
    try:    # network errors do be wildin so lots of try/except
        get_full_balance()
        coins = ['1INCH','BNB','ETH','BTC']
        traders = list()

        for coin in coins:
            traders.append(Trader(coin))

        while True:
            for trader in traders:
                try:    
                    trader.tick()
                except Exception as e:
                    print(e)
                print('==========================')
            time.sleep(60)
    except Exception as e:
        print(e)
