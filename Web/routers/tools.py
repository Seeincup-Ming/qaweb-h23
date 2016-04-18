#coding=utf-8

import sys
import urllib, urllib2
import struct
import socket
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.setdefaultencoding('utf8')
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
#某文件夹下有多少个文件夹
def findalldir(path):
    import os
    listdir=[]
    for item in os.listdir(path):
        itemsrc=os.path.join(path,item)
        #是文件夹则存储
        if os.path.isdir(itemsrc):
            listdir.append(item)
        else:
            pass
    return listdir

#某文件夹下有多少个文件
def findallfile(path):
    import os
    listfile=[]
    for item in os.listdir(path):
        itemsrc=os.path.join(path,item)
        #是文件夹则存储
        if not os.path.isdir(itemsrc):
            listfile.append(item)
        else:
            pass
    return listfile

#获取配置文件所有内容
def getconfig(path):
    import yaml
    configf = open(path)
    x = yaml.load(configf)
    return x['filetypes']

#获取配置文件允许存储的格式
def getaccpttypes(configset):
    accpttypes = []
    for line in configset:
        accpttypes.append(line["type"])
    return accpttypes

#获取配置某种对应文件允许存储个数
def gettypesmaxlen(configpath,types):
    configset = getconfig(configpath)
    for line in configset:
        if line["type"].lower() == types.lower():
            return line["max"]
        
#创建文件夹
def mkdir(path):
    # 引入模块
    import os
    #当前程序运行的位置
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("/")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        #print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print path+' 目录已存在'
        return False
#获取本地文件存储路径
def getfilesavepath(configpath):
    import yaml
    configf = open(configpath)
    x = yaml.load(configf)
    return x["filesave"]["savepath"]

#存储文件到本地并删除多余的文件
def savefile(request,configpath):
    
    from flask import Flask, request
    import os, time


    f = request.files['file']
    fname = f.filename
    savepath = getfilesavepath(configpath)

    fsuffix = fname[fname.rfind('.')+1:].lower()
    fnameonly = fname[:fname.rfind('.')].lower()
    timefoder =  time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    filepath = os.path.join(savepath, fsuffix, fnameonly, timefoder)

    mkdir(filepath)
    #存储到本地
    f.save(os.path.join(filepath, f.filename))
    #删除多余的文件
    import changequeue
    #最多允许存储个数
    maxlen = gettypesmaxlen(configpath,fsuffix)
    
    changequeue.changeq(os.path.join(savepath, fsuffix, fnameonly), maxlen)

#获取页面最大行数
def getpagemaxline(configpath):
    import yaml
    configf = open(configpath)
    x = yaml.load(configf)
    return x["pagemaxline"]["maxline"]

#获取锁状态
def getlockstate(configpath):
    import yaml
    configf = open(configpath)
    x = yaml.load(configf)
    return x["locked"]

#获改变锁状态
def changelockstate(configpath, value):
    import yaml
    configf = open(configpath)
    x = yaml.load(configf)
    x["locked"] = value
    f3=open(configpath,'w')
    yaml.dump(x,stream=f3,default_flow_style=False)    
    return x

def ChangeCoding(s):
    import re,urllib
    s = s.replace('?\\','\\')
    p=re.compile(r'(?P<s>(\\\d\d\d){3,})')
    for i in p.finditer(s):
        old=i.group('s')
        name=old.split('\\')
        name=['%x' %int(g,10) for g in name if g.isdigit() ]
        name='%'+'%'.join(name)
        CN_name= urllib.unquote(name).decode('utf-8')
        s = s.replace(old,CN_name)
    return s

def getchlist(s):
    retlst=[]
    if '\n' in s:
        retlst = s.split('\n')
        retlst = retlst[:-1]
    else:
        retlst.append(s)
    return retlst


def single_msg(addressee = None, msg = ''):
    QA_URL = 'http://qa.nie.netease.com/interface/popo?&'
    para = {'users':addressee,
            'message':msg.encode('gbk')}
    url = QA_URL + urllib.urlencode(para)
    try:
        f = urllib.urlopen(url)
        print f.read(),7777777
        f.close()
    except:
        print 'send single message error'

def group_msg_tcp(team_name, content, address =('10.246.14.83', 8591)):
    #data = u'group_say\ngbk\n'+ team_name +'\n%s'  % content.encode('gbk')
    data = 'group_say\ngbk\n%s\n%s'  % (team_name.decode('utf8').encode('gbk') , content.encode('gbk'))
    data = struct.pack('i', len(data)) + data
    #print content
    #url = "https://10.246.14.83:8088/"
    try:
        #urllib2.urlopen(url,data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.send(data)
        sock.close()
    except Exception, e:
        print str(e)

if __name__ == '__main__':
    #strm = "d:/python_pro/python_upload/static/Uploads/apk/2/2014-11-27-13-54-36/"
    #mkdir(strm)
    print changelockstate('config.yaml',0)
    print getlockstate('config.yaml')
    '''
    CONFIGVALUE = getconfig("config.yaml")
    print "CONFIGVALUE : "
    print CONFIGVALUE
    print getaccpttypes(CONFIGVALUE)
    print gettypesmaxlen(CONFIGVALUE,'IPA3')
    '''



