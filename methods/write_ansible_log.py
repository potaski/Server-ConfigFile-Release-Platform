#!/usr/bin/env python
# coding:utf-8

from db import *

def write_table(dict_in):
    sql = 'insert into playbook_log(task_desc, user,'\
          'group_id, task_log, all_log, run_timestamp,'\
          'log_time) values ("{v1}", "{v2}". "{v3}", '\
          '"{v4}", "{v5}", {v6})'.format(v1=dict_in['task_desc'],
                                         v2=dict_in['user'],
                                         v3=dict_in['group_id'],
                                         v4=dict_in['task_log'],
                                         v5=dict_in['all_log'],
                                         v6=dict_in['run_timestamp']
                                         )
    try:
        cur.execute(sql)
        return 'insert ok'
    except Exception, e:
        with open('/root/tornado.log', 'a') as f:
            f.write(e)
        return 'insert fail, see /root/tornado.log'
