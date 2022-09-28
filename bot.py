import ameritrade

am = ameritrade.api()
print(am.account_info())
print(am.watch_lists())