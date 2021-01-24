import ccxt
import keys

# global exchange information
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': keys.binance_public_key,
    'secret': keys.binance_secret_key,
    'timeout': 30000,
    'enableRateLimit': True
})

def get_full_balance():
    balance = exchange.fetch_balance()
    for coin in balance['info']['balances']:
            if float(coin['free']) > 0:
                name = coin['asset']
                free = coin['free']
                locked = coin['locked']
                print("{0} of {1} free, {2} locked.".format(free, name, locked))

