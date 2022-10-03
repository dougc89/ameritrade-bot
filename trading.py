import os, ameritrade, mongo

class bot_trader:

    def __init__(this, database_name, live = False):

        # are we making live trades?
        this.live = live

        # init the ameritrade api connection
        this.am = ameritrade.api()

        # init account info (we can call it again later)
        this.am.account_info()

        # init the mongo database connection
        this.db = mongo.database(database_name).connection()

        # watchlist (default empty list)
        this.watchlist = []

        # have we got the watchlist yet?
        this.got_watchlist = False

    # this uses the specific watchlist id for the "Bot watchlist" we are using to track potential stocks to buy
    def get_watchlist(this, watchlist_id):

        this.watchlist = this.am.watch_lists(watchlist_id)
        print(this.watchlist)

        # we have obtained the watchlist, to perform operations with
        this.got_watchlist = True

        return this # for chaining

    def check_watchlist(this):
        # check prereqs
        if not this.got_watchlist:
            print('Run get_watchlist before trying to perform operations on it.')
            return False
            
        if len(this.watchlist) < 1:
            print('There do not appear to be any stocks being watched on target watchlist.')
            return False

        # get and store dict of watchlist quotes from ameritrade api
        this.watchlist_quotes = this.am.quotes(this.watchlist)

        for symbol in this.watchlist:
            # check for this stock symbol in our app's version of the watchlist
            if this.db['watchlist'].count_documents({'symbol':symbol, 'enabled': True}) < 1:
                print("Not yet watching {} in app db".format(symbol))
                # init the stock in the watchlist
                this.init_watchlist_item(symbol)
            else: 
                watch_lookup = this.db['watchlist'].find({'symbol':symbol, 'enabled': True})
                for watcher in watch_lookup:
                    # read current price from watchlist_quotes result
                    current_price = this.watchlist_quotes.get(symbol).get('lastPrice')
                    target = watcher.get('buy_limit')
                    print("Target buy price for {symbol} is ${target}. Current price is ${current_price}".format(symbol=symbol, target=target, current_price = current_price))
                    if current_price < target:
                        this.evaluate_purchase(symbol)

    def init_watchlist_item(this, symbol):

        # get the current price of the symbol
        # # quote = this.am.quote(symbol).get(symbol)
        quote = this.watchlist_quotes.get(symbol)
        if quote:
            
            print("Initializing app watchlist for {}".format(symbol))

            current_price = quote.get('lastPrice')
            print("Current price of new stock {} is ${}".format(symbol, current_price))

            # compute the initial buy price limit, with zero consecutive buys
            buy_limit = this.compute_buy_limit(current_price)
            print("Computed buy price of {} as ${}".format(symbol, buy_limit))

            # insert the new record into app watchlist db
            this.db['watchlist'].insert_one({
                'symbol': symbol,
                'description': quote.get('description'),
                'buy_limit': buy_limit,
                'consecutive_buys': 0,
                'enabled': True
            })

        else:
            print("Could not init {}, quote request returned invalid.".format(symbol))

    def compute_buy_limit(this, current_price, consecutive_buys = 0):
        # reduces the next target buy price by 1%, 2%, 4%,... (doubled with each consecutive buy)
        return round( current_price*(1-0.01*pow(2,consecutive_buys)) , 2)

    def evaluate_purchase(this, symbol):
        # return bool for go ahead with purchase
        try:
            # check that we have enough money for the purchase
            current_price = this.watchlist_quotes.get(symbol).get('lastPrice')
            cash_available = this.am.current_balances.get('cashAvailableForTrading')
            # format prices as 2-digit fixed point
            print("There is ${cash_available:.2f} to purchase {symbol} for ${current_price:.2f}".format(symbol=symbol, cash_available=cash_available, current_price=current_price))
            
            # if there is not enough money, fail out
            if current_price > cash_available:
                raise Exception("There is not enough $ available to make that purchase.")

            # now enforce the fact that we don't want to invest more than 2x the percentage of that stock compared to its peers on the watchlist



        except Exception as err:
            print(err)
            return False

    def execute_purchase(this, symbol):
        return True
if __name__ == "__main__": 

    bot = bot_trader('ameritrade_dev') # if we don't specify live = True, we won't make any actual trades
    print(bot.am.positions)
    # bot.get_watchlist(os.getenv('watchlist_id')).check_watchlist()
