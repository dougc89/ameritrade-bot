# ameritrade-bot

## What this is.
This is a casual project by a casual investor, looking to solve the following problems:
* I believe I could make more $$ in the market with constant attention to my portfolio, but do not have the time available in real life to do this.
* With more frequent trading, accruing value from smaller flucuations would be possible. Waiting for larger price changes to trigger trades on manually set limits means missing out on some value that could be extracted from flucuations that did not meet that larger threshold.
* Trading by emotions is a known path to failure in the market. Trading by cold logic will always be better than, as an example, trading by FOMO. Code follows logic with no emotion.

## What this is not.
This project is not the work of a professional stock trader. Any actual trades made based on the logic therein come with the risks of stock market investing; namely the loss of investment funds. If you are willing to take the risks, and the possible rewards, then enjoy the game!!

# Authentication

Do this once:
1. Register for an account with https://developer.tdameritrade.com
1. Create an API app in https://developer.tdameritrade.com/user/me/apps
1. In a web browser, go to https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=https%3A%2F%2Flocalhost&client_id=UAVZQ82D10TQIQZXYDZ4B5VGKY2NSPLY%40AMER.OAUTHAP
How to compute this format:
redirect_uri: the redirect uri that you specified in My Apps (url-encoded). localhost works just fine.
client_id: {{consumer_key}}@AMER.OAUTHAP, where consumer_key is specified under the app details at https://developer.tdameritrade.com/user/me/apps
When you land on this authorization page, you provide the Ameritrade account credentials that you would use to log in to https://www.tdameritrade.com/
Then you will be redirected to your redirect_uri, with the param code={{authorization_code}} << this authorization code is URL-encoded.
Decode it: (e.g. https://www.urldecoder.org/), which replaces the special character %codes with their actual characters.

Then: 
Go to the ameritrade helper website: https://developer.tdameritrade.com/authentication/apis/post/token-0
(They are POSTing to https://api.tdameritrade.com/v1/oauth2/token with the form-urlencoded, but I haven't figured out how to duplicate in Thunderclient yet.)
grant_type: authorization_code
refresh_token: <blank>
access_type: offline
code: {{the auth code that you just decoded. In its decoded form}}
client_id: {{consumer_key from your app; e.g. UAVZQ82D10TQIQZXYDZ4B5VGKY2NSPLY}}
redirect_uri: https://localhost (matching what you specifired in My Apps, but NOT url-encoded)

You should get an HTTP status of 200 with the access (valid for 30 mins) and the refresh (valid for 90 days) tokens. Have fun!
