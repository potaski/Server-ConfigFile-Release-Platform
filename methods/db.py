#!/usr/bin/env python
# coding:utf-8

import MySQLdb


conn = MySQLdb.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='root',
                       db='ansible_log',
                       charset='utf8')
cur = conn.cursor()
