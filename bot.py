import os, ameritrade, mongo

am = ameritrade.api()
# print(am.account_info())

# this uses the specific watchlist id for the "Bot watchlist" we are using to track potential stocks to buy
print(am.watch_lists(os.getenv('watchlist_id')))