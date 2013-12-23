# -*- coding: utf-8 -*-
#/usr/bin/env python

'''
Demo for sinaweibopy
主要实现token自动生成及更新
适合于后端服务相关应用
'''

# api from:http://michaelliao.github.com/sinaweibopy/
from weibo import APIClient

import sys, os, urllib, urllib2
from http_helper import *
from retry import *
try:
    import json
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# weibo api访问配置
#APP_KEY = '2343865591'      # app key
#APP_SECRET = 'aeecb7f044a98be65bf6123195a48b26'   # app secret
CALLBACK_URL = 'http://open.weibo.com/apps/2343865591/info/advanced' # callback url 授权回调页,与OAuth2.0 授权设置的一致
REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
USERID = 'huangyuchenghh@163.com'       # 微博用户名                
USERPASSWD = '123123abc'   # 用户密码

#APP_KEY = '474947209'
#APP_SECRET = '39fb7f503b84986f997aca4861fcd24b'

APP_KEY = '1923992426'
APP_SECRET = '3faca8640c0450ee2f309b6fea76f987'

# token file path  
save_access_token_file  = 'access_token.txt'  
file_path = os.path.dirname(__file__) + os.path.sep  
access_token_file_path = file_path + save_access_token_file  

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET)

def get_access_code():
    '''请求code'''
    params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
        'response_type':'code', \
        'regCallback':'', \
        'redirect_uri':CALLBACK_URL, \
        'client_id':APP_KEY, \
        'state':'', \
        'from':'', \
        'userId':USERID, \
        'passwd':USERPASSWD, \
        })

    login_url = 'https://api.weibo.com/oauth2/authorize'

    url = client.get_authorize_url(CALLBACK_URL)

    content = urllib2.urlopen(url)
    rcode = ''
    if content:
        headers = { 'Referer' : url }
        request = urllib2.Request(login_url, params, headers)
        opener = get_opener(False)
        urllib2.install_opener(opener)
        try:
            f = opener.open(request)
            print f.headers.headers
            for l in f.headers.headers:
                if l.find('Location')==0:
#                    print l
                    rcode = l.split('=')[1]
#                    request = client.request_access_token('cd2a361d12d998ccc2bdd4391559972e',CALLBACK_URL)
#                    access_token = request.access_token
#                    expires_in = request.expires_in
#                    print access_token
#                    print expires_in
#                    client.set_access_token(access_token,expires_in)

        except urllib2.HTTPError, e:
            print "Error code:" ,e.reason
        except urllib2.URLError, e:
            print "Error reason:" ,e.reason

    return rcode.strip('\r\n')

def make_access_token():
    code = get_access_code()
    token = client.request_access_token(code,CALLBACK_URL)

    save_access_token(token)

def save_access_token(token):
    '''将access token保存到本地'''
    f = open(save_access_token_file, 'w')
    f.write(token['access_token']+' ' + str(token['expires_in']))
    f.close()

@retry(1)
def apply_access_token():
    try:
        token = open(save_access_token_file, 'r').read().split()
        if len(token)!=2:
            make_access_token()
            return False
        access_token,expires_in=token
        try:
            client.set_access_token(access_token,expires_in)
        except StandardError, e:
            if hasattr(e, 'error'):   
                if e.error == 'expired_token':  
                    # token过期重新生成  
                    make_access_token()
            else:  
                pass  
    except:
        make_access_token()

    return True

if __name__ == "__main__":
    apply_access_token()
    #code = get_access_code()
    #request = client.request_access_token(code,CALLBACK_URL)
    #    save_access_token(request)
    #    print(client.get.account__rate_limit_status())
    #    status = client.get.account__rate_limit_status()
    #    print json.dumps(status)
    #    status = client.get.account__get_privacy()
    # get followers
    kw = dict(uid=1786678035,count=200)
    status = client.get.friendships__friends(**kw)
    data = json.dumps(status)
    
    
#    token = open(save_access_token_file, 'r').read().split()
#    for (k,v) in status.items():
#        uids = v
        
#        for n in v[10:100]:
#            print 'id:',n['idstr'],'gender:',n['gender'],'bi_followers_count:',n['bi_followers_count']

#        kw2 = dict(access_token=token[0],uids=v[10:20])
#        s = client.get.friendships__friends_chain__followers(**kw2)
            #            print 'follower num:',s['total_number']
        
#    kw3 = dict(uid=1319315934,count=200)
#    status2 = client.get.friendships__followers__active(**kw3)
#    json.dumps(status2)

#    status3 = client.get.trends__hourly()
#    print json.dumps(status3)
#    uid='1786678035'
#    url = "http://weibo.com/u/"+uid
#    req = urllib2.Request(url)
#    req.add_header('Authorization','OAuth %s' % token[0])
#    try:
#        resp = urllib2.urlopen(req)
#        html = resp.read()
#        print html
#    except urllib2.HTTPError, e:
#        raise e

