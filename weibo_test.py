import sys  
import weibo  
import webbrowser
  
#APP_KEY = '3194283051'  
#APP_KEY = '1857001458'  
APP_KEY = '2343865591'
#MY_APP_SECRET = '80b4049df6fb21f88536ca87044dcc2d'  
#MY_APP_SECRET = '59cc72e4af97c891541a485e10a64daf'  
MY_APP_SECRET = 'aeecb7f044a98be65bf6123195a48b26'  
#REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html' 

REDIRECT_URL = 'http://open.weibo.com/apps/2343865591/info/advanced' 
#REDIRECT_URL = 'http://open.weibo.com/apps/2343865591/' 

api = weibo.APIClient(APP_KEY, MY_APP_SECRET)  
  
authorize_url = api.get_authorize_url(REDIRECT_URL)  
  
print(authorize_url)  
  
webbrowser.open_new(authorize_url)  
  
code = raw_input()

request = api.request_access_token(code, REDIRECT_URL)
  
access_token = request.access_token  
  
expires_in = request.expires_in  

print access_token
print expires_in
api.set_access_token(access_token, expires_in)  

#print(api.statuses__public_timeline())
print(api.statuses__home_timeline())
