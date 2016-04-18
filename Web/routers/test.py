# -*- coding:utf-8 -*-
import urllib,urllib2
import time


URL = 'http://10.246.13.195:8000/issues/create'
info = {"author":"hzwanpeng"}

pmsgs = u'发现bug：11111111111111111111111111'
def grab_bug(info, stype, sender, pmsg, writer):
    pmsg = pmsg[5:]
    pmsg = pmsg.strip(u',，:： \t')
    values = {
        'content': pmsg.encode('utf-8'),
        'author': info['author'],
        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    print values
    data = urllib.urlencode(values)
    print data
    request = urllib2.Request(URL, data)
    response = urllib2.urlopen(request)
    result = response.read()
    print result
    try:
        if result == '1':
            print '11111111111'
        else:
            raise ValueError
    except:
        print 22222222222222222
        #writer.write(u"BUG上传失败\n")

grab_bug(info ,stype = None,sender=None, pmsg =pmsgs ,writer=None)
