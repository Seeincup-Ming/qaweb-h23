# -*- coding: utf-8 -*-
import tools,os,re,copy
import flask,time
from flask import request, flash, redirect, url_for, render_template

import models
#from tools import popointerface


#import rpc
config_path = './routers/config.yaml'
bp = flask.Blueprint('svnlock', __name__)
maxline = tools.getpagemaxline(config_path)
lockroute = [u'program_clone',u'导入数据']


@bp.route('/getstate', methods=['GET'])
def getwitchstate():
     if request.method == 'GET':
         return str(tools.getlockstate(config_path))

@bp.route('/masterswitch', methods=['GET', 'POST'])
@models.db_session
def masterswitch():
    try:
        setvalue = int(request.args.get('id', 2))    # 获取GET参数，没有参数就赋值 0
    except ValueError:
        abort(404)      # 返回 404
    if not(setvalue in [0,1,2,3]):
        return '参数错误'

    if request.method == 'GET':
        if tools.getlockstate(config_path) == 1:
            state = "不允许上传"
        else:
            state = "允许上传"
        if setvalue == 2:#显示当前状态
            if request.remote_addr == '10.246.14.83':
                return render_template('masterswitch.html',\
                                   state1 = state,\
                                   locked = str(1))
            return render_template('masterswitch.html',\
                                   state1 = state,\
                                   locked = str(tools.getlockstate(config_path)))
        elif setvalue in [0,1]:#更改当前状态
            tools.changelockstate(config_path,setvalue)
            return redirect(url_for('masterswitch',\
                                    id = 2), 302)
        elif setvalue == 3:#清空数据库
            alldata = boxes = models.select(b for b in models.Svndb)[:]
            for somedata in alldata:
                somedata.delete()
            return 'all data delete'
        else:
            return 'error par'


    elif request.method == 'POST':
        from werkzeug.datastructures import ImmutableMultiDict
        if tools.getlockstate(config_path) == 1:
            state = "不允许上传"
        else:
            state = "允许上传"
        templist = copy.deepcopy(request.form)
        sss = copy.copy(str(templist['path']))
        print type(sss)
        sss = tools.ChangeCoding(sss)
        print sss,111111111111111111
        #templist['path']  = chiesestr
        #print templist['path']
        if not lockroute:
            return render_template('masterswitch.html',\
                                   state1 = state,\
                                   locked = str(tools.getlockstate(config_path)))
        else:
            for locked in lockroute:
                print locked
                reroute = re.compile(locked)
                print reroute.search(sss)
                if reroute.search(sss):
                    if tools.getlockstate(config_path) == 1:
                        state = 0
                    else:
                        state = 1
                    return render_template('masterswitch.html',\
                                   state1 = state,\
                                   locked = str(tools.getlockstate(config_path)))
            return render_template('masterswitch.html',\
                                   state1 = state,\
                                   locked = str(0))
        '''
        if tools.getlockstate(config_path) == 1:
            state = 0
        else:
            state = 1

        if templist.has_key('changestate'):
            return redirect(url_for('masterswitch',\
                                    id = state), 302)
        else:
            pass

        return state'''


@bp.route('/svncode', methods=['GET','POST'])
@models.db_session
def svncode():
    #from DB import engine,svnset
    #from sqlalchemy.orm import sessionmaker
    #Session = sessionmaker(bind=engine)
    #session = Session()

    if request.method == 'GET': #查找

        lista=[]
        alldata = models.select(b for b in models.Svndb )[:]
        #alldata = session.query(svnset).all()
        for somedata in alldata:
            dicta={}
            dicta['author'] = somedata.author
            dicta['change'] = somedata.change
            dicta['diff'] = somedata.diff
            dicta['md5'] = somedata.md5
            dicta['lock_flag'] = bool(somedata.lock_flag)
            lista.append(dicta)
        return repr(lista)
    else:#存储 POST
        from werkzeug.datastructures import ImmutableMultiDict
        templist = request.form
        if templist.has_key('md5'): #存储数据
            #print templist['md5']
            alldata = models.select(S for S in models.Svndb if S.change ==  templist['change'] and S.md5 == templist['md5'])[:]
            '''
            alldata = session.query(svnset).filter(\
                            #svnset.name == templist['name'], \
                            svnset.change == templist['change'], \
                            #svnset.diff == templist['diff'], \
                            svnset.md5 == templist['md5']).all()
                            '''
            if alldata:
                for line in alldata:
                    #返回存储值状态0,1,2
                    #print unicode(line.change).encode('gbk')
                    if str(line.lock_flag) == '0':
                        line.delete()
                        #session.commit()
                    return str(line.lock_flag)
            else:#没有这条数据，存储下来，返回3
                #a = templist['change']
                #chtemp = tools.ChangeCoding(a)
                #for ch in lockroute:
                    #if re.compile(ch).search(chtemp):
                        #svnset = models.Svndb(change=templist['change'], author=templist['name'],diff = templist['diff'],md5 =templist['md5'],lock_flag = '2' )
                    #else:
                        #svnset = models.Svndb(change=templist['change'], author=templist['name'],diff = templist['diff'],md5 =templist['md5'],lock_flag = '0' )
                create = time.strftime('%Y-%m-%d %H:%M:%S')
                #print templist['log'],'logs'
                #print templist['diff'],'diffs'
                svnset = models.Svndb(change=templist['change'], author=templist['name'],diff = templist['diff'],md5 =templist['md5'],lock_flag = '2',log = templist['log'],creattime = unicode(create))
                alldatalist  = models.select(b for b in models.Svndb )[:]
                print len(alldatalist),'length1'
                content = '有一条来自'.decode('utf8')+templist['name']+ u'的新提交，请尽快处理。\r\nlogs: '+tools.ChangeCoding(templist['log'])
                #############################此处可添加popo提醒###########################################
                return '3'
        else:
            return 'wrong data'

#SVNGET页面显示
@bp.route('/svnview/<pageindex>', methods=['GET','POST'])
@models.db_session
def svnview(pageindex):
    alldatalist  = models.select(b for b in models.Svndb )[:]
    print len(alldatalist),'length'
    totalpage = (len(alldatalist)+maxline-1)/maxline
    alldatalist = alldatalist
    index = (int(pageindex)-1)*10
    listview = []
    cnt = 0
    cntindex = index
    while cntindex < len(alldatalist) and cnt < maxline:
        dicta={}
        dicta['author'] = alldatalist[cntindex].author
        dicta['creattime'] = alldatalist[cntindex].creattime
        chiesestr = tools.ChangeCoding(alldatalist[cntindex].change)
        dicta['change'] = tools.getchlist(chiesestr.encode('utf8'))
        dicta['change'] = '<br/>'.join(dicta['change'])
        chiesestr = tools.ChangeCoding(alldatalist[cntindex].log)
        dicta['log'] = tools.getchlist(chiesestr.encode('utf8'))
        dicta['log'] = '<br/>'.join(dicta['log'])
        #dicta['change'] = alldatalist[cntindex].change
        dicta['md5'] = alldatalist[cntindex].md5
        #print dicta['md5'].encode('gbk')
        lockstate = ""
        if alldatalist[cntindex].lock_flag == '0':
            lockstate = "允许提交"
        elif alldatalist[cntindex].lock_flag == '1':
            lockstate = "不允许提交"
        else:
            lockstate = "未审查"

        dicta['lock_flag'] = lockstate
        dicta['index'] = cntindex
        listview.append(dicta)
        cntindex = cntindex + 1
        cnt = cnt + 1
    if request.method == 'GET':
        return render_template('svnlock.html',\
                               posts1 = listview, \
                               posts2 = "",\
                               now = int(pageindex),
                               total = totalpage)
    elif request.method == 'POST':
        #from werkzeug.datastructures import ImmutableMultiDict
        templist = request.form

        if templist.has_key('next'): #下一页
            gotopage = 0
            if int(templist['nowpage']) < totalpage:
                gotopage = int(templist['nowpage']) + 1
            else:
                gotopage = int(templist['nowpage'])
            return redirect('/svnlock/svnview'+'/'+str(gotopage))
        elif templist.has_key('previous'): #上一页
            gotopage = 0
            if int(templist['nowpage']) > 1:
                gotopage = int(templist['nowpage']) -1
            else:
                gotopage = int(templist['nowpage'])
            return redirect('/svnlock/svnview'+'/'+str(gotopage))
        elif templist.has_key('submitchange'): #修改状态
            state = templist['changestate']
            gotopage = templist['nowpage']
            if templist.has_key('users'):
                userindexlst = templist.getlist('users')
                for userindex in userindexlst:
                    #alldatalist = models.select(S for S in models.Svndb if S.change ==  templist['change'] and S.md5 == templist['md5'])[:]
                    if state == '2':
                        alldatalist[int(userindex)].delete()
                    else:
                        alldatalist[int(userindex)].lock_flag=state
                    print alldatalist[int(userindex)].lock_flag , alldatalist[int(userindex)].change
            return redirect('/svnlock/svnview'+'/'+gotopage)

@bp.route('/lock')
def unlock():
    try:
        tools.changelockstate(config_path,1)
        return 'succeed'
    except:
        return 'something wrong '

@bp.route('/unlock')
def lock():
    try:
        tools.changelockstate(config_path,0)
        return 'succeed'
    except:
        return 'something wrong '

@bp.route('/clear')
@models.db_session
def clear():
    try:
        alldatalist  = models.select(b for b in models.Svndb )[:]
        for data in alldatalist:
            data.delete()
        return 'succeed'
    except Exception,e:
        print e
        return 'something wrong '


