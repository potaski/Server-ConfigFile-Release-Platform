#!/usr/bin/env python
# coding:utf-8

import tornado.web
import os
import commands
import json
import methods.playbook_log as pb_log
import time
from multiprocessing import Process


def run_playbook(group_id):
    playbook_dir = '/etc/ansible'
    playbook = '{dirs}/{group_id}.yml'.format(dirs=playbook_dir,
                                              group_id=group_id)
    if os.path.isfile('/root/anaconda-ks.cfg'):
        # cmd = '/home/zhangwei/pb/run_pb.py --playbook={}.yml'.format(playbook)
        cmd = '/home/zhangwei/pb/run_pb.py --playbook=/home/zhangwei/pb/test.yml'
        (cmd_state, cmd_out) = commands.getstatusoutput(cmd)
        
        if cmd_state == 0:
            '''
            analysis json get log
            store log to mysql
            store json to http://{ip}/statics/playbook/{id}.json
            store json url to mysql
            '''

            
        else:
            return None


class PlaybookAPI(tornado.web.RequestHandler):

    def get(self):
        """
        http get method, use in playbook auto run
        """
        task_desc = 'Tianya System Change'
        user = 'Ansible'
        group_id = self.get_argument('group_id')
        run_time = str(time.time())

        # check time, only run in week: 2 or 4, hour: 08:30-09:00
        week = int(time.strftime('%w'))
        hour = int(time.strftime('%H%M'))
        is_exec = False
        if week == 2 or week == 4:
            if hour > 829 or hour < 900:
                # run pb
                is_exec = True

        is_exec = True
        if is_exec:
            res_json = run_playbook(group_id)
            if res_json:
                dict_insert = {'task_desc': task_desc,
                               'user': user,
                               'group_id': group_id,
                               'task_log': 'null',
                               'all_log': res_json,
                               'run_timestamp': run_time}
                res = pb_log.write_table(dict_insert)
                out_string = '{}<br>{}'.format(group_id, res)
                self.write(res)
            else:
                self.write('get error')
        else:
            self.write('time is not right')

    
    """
    def get(self):
        # http://192.168.1.1/playbook?group_id=xxx
        group_id = self.get_argument('group_id')
        playbook = '/etc/ansible/ansible_playbook/{id}.yml'.format(id=group_id)
        cmd = '/home/zhangwei/pb/run_pb.py --playbook=/home/zhangwei/pb/test.yml'
        (cmd_state, cmd_out) = commands.getstatusoutput(cmd)
        out_string = '{group_id}<br>{cmd_state}<br>{cmd_out}'.format(group_id=group_id,
                                                                     cmd_state=cmd_state,
                                                                     cmd_out=cmd_out)
        self.write(out_string)
    """

