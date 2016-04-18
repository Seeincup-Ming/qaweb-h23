#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pony.orm import *
from datetime import datetime, timedelta, date
import json

#sql_debug(True)
db = Database()

# for h15 only 2014-09-05
class Svndb(db.Entity):
    change = Required(unicode, unique=True)
    author = Optional(unicode)
    diff = Optional(unicode)
    md5 = Optional(unicode)
    lock_flag = Optional(unicode)
    #description = Optional(unicode)
    #host = Optional(unicode)
    log = Optional(unicode)
    creattime = Optional(unicode)
    #ports = Set("BoxPort")

class Bugs(db.Entity):
    content = Required(unicode, unique=True)
    author = Optional(unicode)
    time = Optional(unicode)


'''
class BoxPort(db.Entity):
    local = Required(int)
    container = Required(int)
    box = Optional(Box)
'''
db.bind('sqlite', './test_db.sqlite', create_db=True)
#db.bind('mysql', host='mt.nie.netease.com', user='box', passwd='box', db='box')
db.generate_mapping(create_tables=True)

