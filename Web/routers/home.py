# -*- coding: utf-8 -*-
import datetime
import random
import time,os
import threading
import json
import urllib2,urllib
import flask
from flask import request, flash, redirect, url_for, render_template
import models
#import rpc


bp = flask.Blueprint('home', __name__)


@bp.route('/')
def home():
    url = "http://10.246.13.194:8000/serverlist"
    try:
        # req = urllib2.Request(url)
        # response = urllib2.urlopen(req,timeout = 30)
        #
        # res = json.loads(response.read())
        # boxes = res.get('data')
        # print boxes
        return render_template('box.html')
    except Exception,e:
        print e
        return 'failure'

    #return 'welcome to H20 QAtools'
'''
@bp.route('/download/<filename>')
def down_apk(filename):
    if filename == 'apk':
        path = '/home/hzwanpeng/program_apk/runtime/android'
        filename = 'H20-debug.apk'
        return flask.send_from_directory(path,filename,as_attachment = True)
    elif filename == 'stable':
        path = '/home/hzwanpeng'
        filename = 'H20-stable.apk'
        return flask.send_from_directory(path,filename,as_attachment = True)
'''


@bp.route('/gmcom')
def gmcom():
    robot_txt = '/home/hzwanpeng/program/robot/popo_robot/plugin/update_bag/robot.txt'
    os.system('svn up %s' % robot_txt)
    f = open(robot_txt)
    gm = f.read()
    gmlist = gm.split('\n')
    return render_template('gm.html',gm =gmlist)


@bp.route('/serverup')
def serverup():
    url = "http://10.246.13.194:8000/serverlist"
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req,timeout = 30)

        res = json.loads(response.read())
        boxes = res.get('data')
        print boxes
        return render_template('server_up.html', boxes=boxes)
    except Exception,e:
        print e
        return 'failure'

@bp.route('/download',methods=['POST', 'GET'])
def download():
    filename = request.args.get('inlineRadioOptions')
    if filename == 'apk':
        path = '/home/hzwanpeng/program_apk/publish/android'
        filename = 'H20-release-signed.apk'
        return flask.send_from_directory(path,filename,as_attachment = True)
    elif filename == 'stable':
        path = '/home/hzwanpeng'
        filename = 'H20-stable.apk'
        return flask.send_from_directory(path,filename,as_attachment = True)
    else:
        return 'failure'


@bp.route('/upserver/<docker_id>',methods=['POST', 'GET'])
def update(docker_id):
    kerrevi = request.form.get('kerrevi')
    serrevi = request.form.get('serrevi')
    print kerrevi
    print serrevi
    url = "http://10.246.13.194:8000/api/up2revi/"+docker_id+'/'+serrevi+'/'+kerrevi
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req,timeout = 30)
        res = response.read()
        return 'succeed'
    except Exception,e:
        print e
        return "failure"
    #return 'welcome to H20 QAtools'''''


@bp.route('/issues/create',methods=['POST', 'GET'])
@models.db_session
def create_bug():
    try:
        if request.method == 'POST':
            templist = request.form
            #print templist,222222222222222222222222222
            #print templist.get('content'),3333333333333
            alldata = models.select(S for S in models.Bugs if (S.author ==  templist.get('author') and S.content == templist.get('content')))[:]
            if not alldata:
                bug = models.Bugs(content=templist.get('content'))
                bug.author=templist.get('author')
                bug.time = templist.get('time')
        return '1'
    except Exception,e:
        print e
        return '2'

@bp.route('/show/bugs')
@models.db_session
def show_bugs():
    alldatalist  = models.select(b for b in models.Bugs )[:]
    return render_template('bugs.html',bugs = alldatalist)
    #return 'welcome to H20 QAtools'''''

# @bp.route('/svnlock/svnview/1')
#
# def showsvnlock():
#      return render_template('svnlock.html')


@bp.route('/clear/bugs')
@models.db_session
def clear_bugs():
    alldatalist  = models.select(b for b in models.Bugs )[:]
    for bug in alldatalist:
        bug.delete()
    return 'succeed'
    #return 'welcome to H20 QAtools'''''