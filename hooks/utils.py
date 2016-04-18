#coding=utf-8

import os, sys
import urllib 
import urllib2


class resp:
    def __init__(self, txt=None):
        self.text = txt
   
def web_post(url, data):
    try:
        req = urllib2.Request(url) 
        data = urllib.urlencode(data) 
        #enable cookie 
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
        response = opener.open(req, data)
    except:
        return None
    return resp(response.read())

def web_get(url):
    try:
        req = urllib2.urlopen(url)
    except:
        return None
    return req.read()

def setlocale():
    import locale
    language_code, encoding = locale.getdefaultlocale()
    if language_code is None:
        language_code = 'zh_CN'
    if encoding is None:
        encoding = 'UTF-8'
    if encoding.lower() == 'utf':
        encoding = 'UTF-8'
    locale.setlocale(locale.LC_ALL, '%s.%s'%(language_code, encoding))

def get_cmd_output(cmd):
    r = os.popen(cmd)
    return r.read()

def get_svnlook():
    platform = sys.platform
    if platform.startswith('win'):
        return get_cmd_output(['where svnlook']).split('\n')[0].strip()
    return 'svnlook'

def svnlook(lookfor, path, arg, txn):
    cmd = [get_svnlook(), lookfor, path, arg, txn]
    return cmd

def execcmd(cmd):
    return os.popen(' '.join(cmd)).read()
