# -*- coding: utf-8 -*-
# 

import sys
import os
import urllib
import urllib2


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

class WeiboClient(object):
    # initiate client 
    # child will derivered them
    
    def __init__(self,appkey='',appsecret='',access_token='',expires_in='',uid='',original_data=''):
        
        pass
    
    
    pass
