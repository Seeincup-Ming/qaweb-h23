#coding=utf-8

import sys
import md5
from utils import *
import website
import requests

'''
QAWeb = 'http://127.0.0.1:5000/'
locks = 'svncode'
switch = 'masterswitch'
'''
QAWeb = website.Web['index']
locks = website.Web['locks']
switch = website.Web['switch']


if __name__ == '__main__':
    repo = sys.argv[1]
    txn = sys.argv[2]
    #repo = ''
    #setlocale()
    #sys.exit(0)

    #make svnlook cmds
    changed_cmd = svnlook('changed', repo, '-t', txn)
    diff_cmd = svnlook('diff', repo, '-t', txn)
    author_cmd = svnlook('author', repo, '-t', txn)
    log_cmd = svnlook('log', repo, '-t', txn)

    #get svnlook cmds output
    author = execcmd(author_cmd)
    changed = execcmd(changed_cmd)
    diff = execcmd(diff_cmd)
    log = execcmd(log_cmd)


    md5val = md5.new(author + changed).digest()

    #get the main lock switch status
    path_info = {'path':changed}
    try:
        #switch_state = requests.get(url=(QAWeb + switch))
        switch_state = requests.post(url=(QAWeb + switch), data=path_info,timeout = 5)
    except:
        sys.exit(0)

    if switch_state.status_code != 200:
        #if cannot get the web response, pass the commit
        sys.exit(0)
    txt = switch_state.text.encode('utf-8')
    if txt.find('locked=0') >= 0:
        #main switch is off, which means the svn is not locked
        sys.exit(0)

    #make the lock info dict
    new_lock = {
        'name':author,
        'change':changed,
        'diff':diff,
        'log':log,
        'md5':md5val,
    }

    #post the new commit info, the web will handle it and return a lock status code
    try:
        ret = requests.post(url=(QAWeb + locks), data=new_lock,timeout = 5)
    except:
        sys.exit(0)

    '''

    0: commit is confirmed and passed
    1: commit is rejected
    2: commit is being handled
    3: first commit
    default: error status, reject the commit
    '''

    if ret.text == '0':
        sys.stderr.write('commit passed\n')
        sys.exit(0)
    elif ret.text == '1':
        sys.stderr.write('commit rejected\n')
        sys.exit(1)
    elif ret.text == '2':
        sys.stderr.write('commit being handling\n')
        sys.exit(1)
    elif ret.text == '3':
        sys.stderr.write('new commit, please wait for handling\n')
        sys.exit(1)
    else:
        sys.stderr.write('sys error, please contact QA\n')
        sys.exit(1)
    sys.exit(1)  
