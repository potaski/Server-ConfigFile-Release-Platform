#!/usr/bin/env python
# coding:utf-8

import MySQLdb


conn = MySQLdb.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='Something999!',
                       db='ansible',
                       charset='utf8')
cur = conn.cursor()
