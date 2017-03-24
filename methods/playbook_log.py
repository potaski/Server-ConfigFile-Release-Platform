#!/usr/bin/env python
# coding:utf-8

from db import *


def write_table(dict_in):
    sql = '''insert into playbook_log (task_desc, user, group_id, all_log, run_timestamp)
values ("{v1}", "{v2}", "{v3}", "'{v4}'", "{v5}")'''.format(v1=dict_in['task_desc'],
                                                          v2=dict_in['user'],
                                                          v3=dict_in['group_id'],
                                                          v4=dict_in['all_log'],
                                                          v5=dict_in['run_timestamp'])
    cur.execute(sql)
    return sql
