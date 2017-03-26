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
            cmd_out = cmd_out.split('.retry\n')[-1]
            return cmd_out
            
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
                               'all_log': res_json,
                               'run_timestamp': run_time}
                insert_res = pb_log.write_table(dict_insert)
                if insert_res:
                    out_string = """<html><head><title>稍候。。。</title></head>
<body>
<script language='javascript'>document.location = 'http://192.168.71.128/ansible/log?group_id={}&run_timestamp={}'</script>
</body>
</html>""".format(group_id, run_time)
                    self.write(out_string)
            else:
                self.write('get error')
        else:
            self.write('time is not right')

 
class QueryPlaybookResult(tornado.web.RequestHandler):

    def get(self):
        dict_args = {}
        dict_args['group_id'] = self.get_body_argument('group_id')        
        dict_args['run_timestamp'] = self.get_body_argument('run_timestamp')
        try:
            json_log = pb_log.read_table(dict_args)
            if json_log:
                # analysis json log and create html page 

