#!/usr/bin/env python
# coding:utf-8

from db import *

def select_table(table, column, condition, value):
    sql = "select {} from {} where {}='{}'".format(column,
                                                   table,
                                                   condition, 
                                                   value) 

    cur.execute(sql)
    lines = cur.fetchall()
    return lines
