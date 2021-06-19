from exchange import exchange
import os.path
import json

# class to trade on specified symbol
class Trader:
    coin = str()
    symbol = str()
    usdt_balance = float()
    coin_balance = float()
    previous_bid = float()
    previous_ask = float()

    # init function gets buy and sell prices on startup and our balance of the coin this instance should trade on
    def __init__(self, coin):
        self.coin = coin
        self.symbol = self.coin + '/USDT'
        info = exchange.fetch_ticker(self.symbol)
        self.previous_bid = float(info['bid'])
        self.previous_ask = float(info['ask'])
        print('Buy price of ' + coin + ': {}'.format(self.previous_bid))
        print('Sell price of ' + coin + ': {}'.format(self.previous_ask))
        self.get_balances()

    def get_balances(self):
        balance = exchange.fetch_balance()
        for coin in balance['info']['balances']:
            if float(coin['free']) > 0:
                name = coin['asset']
                free = coin['free']
                if name == 'USDT':            
                    self.usdt_balance = float(free)
                    print('Balance of USDT is ' + free)
                elif name == self.coin:            
                    self.coin_balance = float(free)
                    print('Balance of {0} is {1}'.format(self.coin, free))

    # call this to check the changes in prices since last tick, and execute trades if you want to
    def tick(self):    
        self.get_balances()   
        info = exchange.fetch_ticker(self.symbol)
        bid = float(info['bid'])   # buy price        
        ask = float(info['ask'])   # sell price
        print('Bid price of {0} is: {1}'.format(self.coin, bid))
        print('Ask price of {0} is: {1}'.format(self.coin, ask))

        # this is suuuper basic, basically every tick check the prices
        # if the buy price is down 8% since the last time we bought, buy a for 25% of our USDT balance
        # if the buy price is down at all, buy a very small amount
        # if the sell price is up 8% since the last time we bought, sell everything we have
        # if the sell price is up at all, sell a small amount
                
        if ask >= (self.previous_ask * 1.04):
            try:                    
                response = exchange.create_order(self.symbol, 'market', 'sell', self.coin_balance)
                print('Created sell all order {0} on {1}'.format(response['id'], self.symbol))
                id = response['id'] + '-SELL_ALL.json'                    
                with open(os.path.join('orders/', id), 'w') as file:
                    file.write(json.dumps(response))  
                self.previous_bid = bid # record buy price at the time we sell, so that we only buy more if its less than what we last sold for - does that make sense?  
                self.get_balances()                                
            except Exception as e:
                print('Error occured selling all on ' + self.symbol)
                print(e)                                          
        else:
            print('Curret sell price is not less than previous one, returning...') 

        if ask > self.previous_ask:
            if self.coin_balance >= (11 / ask):
                try:                    
                    response = exchange.create_order(self.symbol, 'market', 'sell', (self.coin_balance * 0.25) if (self.coin_balance > 44 / ask) else (12 / ask))
                    print('Created sell order {0} on {1}'.format(response['id'], self.symbol))
                    id = response['id'] + '-SELL.json'                    
                    with open(os.path.join('orders/', id), 'w') as file:
                        file.write(json.dumps(response))         
                    self.previous_bid = bid           
                    self.get_balances()
                except Exception as e:
                    print('Error occured selling on ' + self.symbol)
                    print(e)                                    
            else:
                print(self.coin + ' balance too low to sell...')  
        
        if bid < (self.previous_bid * 0.92):
            if self.usdt_balance >= 11: 
                try:                    
                    response = exchange.create_order(self.symbol, 'market', 'buy', ((self.usdt_balance * 0.25) / bid) if (self.usdt_balance >= 44) else (11 / bid))
                    print('Created buy order {0} on {1}'.format(response['id'], self.symbol))
                    id = response['id'] + '-BUY.json'  
                    with open(os.path.join('orders/', id), 'w') as file:
                        file.write(json.dumps(response))
                    self.previous_bid = bid
                    self.previous_ask = ask # remember what the sell price is only when we buy, as that is the value of our coin
                    self.get_balances()
                except Exception as e:
                    print('Error occured buying large on ' + self.symbol)
                    print(e)                    
                    return
            else:
                print('USDT balance too low to buy large...')            
        elif bid < self.previous_bid:
            if self.usdt_balance >= 11: 
                try:                    
                    response = exchange.create_order(self.symbol, 'market', 'buy', 11 / bid)
                    print('Created buy order {0} on {1}'.format(response['id'], self.symbol))
                    id = response['id'] + '-BUY.json'  
                    with open(os.path.join('orders/', id), 'w') as file:
                        file.write(json.dumps(response))
                    self.previous_bid = bid
                    self.previous_ask = ask # remember what the sell price is only when we buy, as that is the value of our coin
                    self.get_balances()
                except Exception as e:
                    print('Error occured buying on ' + self.symbol)
                    print(e)                    
                    return
            else:
                print('USDT balance too low to buy...')            
        else:
            print('Current buy price is not less than previous one, checking sell price...')
        
        
         

