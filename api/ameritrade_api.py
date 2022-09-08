import os, credentials, requests

def connect():
    auth_config = {'client_id': os.getenv('ameritrade_client_id'), 'grant_type': 'refresh_token', 'refresh_token': os.getenv('refresh_token')}
    r = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=auth_config)
    if (r.status_code == 200):
        access_token = r.json().get('access_token')
        print(access_token)
        headers = {'Authorization': "Bearer {}".format(access_token)}
        q = requests.get("https://api.tdameritrade.com/v1/accounts/{}".format(os.getenv('ameritrade_account_id')), headers=headers)
        print(q.status_code)
        print(q.json())
        return q.json()
    else:
        print('connection issue')
        return False

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    api = connect()
    print(api)