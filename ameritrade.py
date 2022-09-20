import os, credentials, requests

class api:
    token = None

    def __init__(this):
        auth_config = {'client_id': os.getenv('ameritrade_client_id'), 'grant_type': 'refresh_token', 'refresh_token': os.getenv('refresh_token')}
        r = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=auth_config)
        if (r.status_code == 200):
            this.token = r.json().get('access_token')
            # print(this.token)
        else:
            print('connection issue')

    def account_info(this):
        headers = {'Authorization': "Bearer {}".format(this.token)}
        q = requests.get("https://api.tdameritrade.com/v1/accounts/{}".format(os.getenv('ameritrade_account_id')), headers=headers)
        print(q.status_code)
        print(q.json())
        return q.json()

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    am = api()
    # print(am.token)
    print(am.account_info())