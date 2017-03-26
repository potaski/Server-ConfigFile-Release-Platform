#!/usr/bin/env python
# coding:utf-8

from db import *


def write_table(dict_in):
    sql = '''insert into playbook_log (task_desc, user, group_id, all_log, run_timestamp)
values ("{v1}", "{v2}", "{v3}", '{v4}', "{v5}")'''.format(v1=dict_in['task_desc'],
                                                          v2=dict_in['user'],
                                                          v3=dict_in['group_id'],
                                                          v4=dict_in['all_log'],
                                                          v5=dict_in['run_timestamp'])
    try:
        res = cur.execute(sql)
        conn.commit() 
        return True
    except:
        return False


def read_table(dict_in):
    sql = '''select all_log from playbook_log where group_id="{v1}"
 and run_timestamp="{v2}"'''.format(v1=dict_in['group_id'],
                                    v2=dict_in['run_timestamp'])
    try:
        cur.execute(sql)
        res = cur.fetchall()
        return str(res[0][0])
    except:
        return False
                            
