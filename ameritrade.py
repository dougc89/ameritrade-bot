import os, credentials, requests

class api:
    # we have to init with obtaining a temporary access token, using our refresh token
    token = None

    # default auth headers, using a Bearer {{token}}
    auth = {}

    # static ameritrade account identifiers pulled from env, for ease of reference
    client_id = None
    account_id = None

    # live account info, read from api
    account_info_data = None
    watch_lists_data = None
    # focused watchlist
    watch_list = []


    def __init__(this):
        # set local version of ameritrade account info
        this.account_id = os.getenv('ameritrade_account_id')
        this.client_id = os.getenv('ameritrade_client_id')

        # prepare access token request
        auth_config = {'client_id': this.client_id, 'grant_type': 'refresh_token', 'refresh_token': os.getenv('refresh_token')}
        q = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=auth_config)
        if (q.status_code == 200):
            this.token = q.json().get('access_token')
            this.auth = {'Authorization': "Bearer {}".format(this.token)}
            # get basic account info
            this.account_info()
            # print(this.token)
        else:
            print('issue obtaining access token')

    def account_info(this):
        # return account info if we already have it
        if this.account_info_data:
            return this.account_info_data

        # obtain account info via api
        q = requests.get("https://api.tdameritrade.com/v1/accounts/{account_id}".format(account_id = this.account_id), headers=this.auth)
        # print(q.status_code)
        
        if q.status_code == 200:
            # print(q.json())
            this.account_info_data = q.json().get('securitiesAccount')
            # print(this.account_info_data.get('currentBalances'))
            # set current balances object so that we can recall it later
            this.current_balances = this.account_info_data.get('currentBalances')
            return this.account_info_data
            # return this # for chaining
        else: 
            print('issue obtaining account info')
            return False

    def watch_lists(this, id = None):
        # id is an optional argument to request a specific watchlist, otherwise we just get all watchlists on the account in a list
        q = requests.get("https://api.tdameritrade.com/v1/accounts/{account_id}/watchlists".format(account_id = this.account_id), headers=this.auth)
        
        if q.status_code == 200:
            # print(q.json())
            this.watch_lists_data = q.json()

            # set watch list as simplified list of watch list items
            this.watch_list = []
            for item in this.watch_lists_data[0].get('watchlistItems'):
                this.watch_list.append(item.get('instrument').get('symbol'))

            return this.watch_list
            # return this # for chaining
        else: 
            print('issue obtaining watch lists')
            return False
    
    def quotes(this, symbols = []):
        # symbols is a list of the symbols we want to get the price quotes for

        # concat array to string, comma-separated list
        symbol_list = ','.join(symbols)

        q = requests.get("https://api.tdameritrade.com/v1/marketdata/quotes?symbol={symbol_list}".format(symbol_list = symbol_list), headers=this.auth)
        if q.status_code == 200:
            # print(q.json())
            return q.json()
        else: 
            print('issue obtaining stock quotes')
            return False

    def quote(this, symbol):
        # symbols is a str, one symbol only. Use this.quotes for list of symbols

        q = requests.get("https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes".format(symbol = symbol), headers=this.auth)
        if q.status_code == 200:
            # print(q.json())
            return q.json()
        else: 
            print('issue obtaining stock quotes')
            return False

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    am = api()
    # print(am.token)
    # print(am.account_info())
    # print(am.watch_lists())
    print(am.quote('AAPL'))