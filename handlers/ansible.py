#!/usr/bin/env python
# coding:utf-8

import tornado.web
import os
import commands
import json
from multiprocessing import Process


class AnsiblePlaybook(tornado.web.RequestHandler):
    
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

