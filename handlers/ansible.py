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

            
def playbook_callback_analysis(pb_json):
    dict_ip2log = {}
    
    j = json.loads(str(pb_json))

    aa = j['plays']
    ab = aa[0]['tasks']

    for element in ab:
        dict_task2state = {}
        task_name = element['task']['name']
        
        if task_name == '':
            # facter state
            task_name = 'facter'
            facter_result = element['hosts']
            dict_state2info = {}
            
            for ip, res in facter_result.items():
                try:
                    dict_state2info['is_unreachable'] = str(res['unreachable'])
                except:
                    pass
                try:
                    dict_state2info['is_changed'] = str(res['changed'])
                except:
                    pass
                try:
                    dict_state2info['msg'] = str(res['msg']).strip()
                except:
                    pass
                    
            dict_task2state[str(task_name)] = dict_state2info
            dict_ip2log[str(ip)] = dict_task2state
            continue
                    
        else:
            # task state
            task_result = element['hosts']
            dict_state2info = {}
            
            for ip, res in task_result.items():
                try:
                    dict_state2info['is_skipped'] = str(res['results'][0]['skipped'])
                except:
                    dict_state2info['is_skipped'] = 'False'
                dict_state2info['is_changed'] = str(res['changed'])
                try:
                    dict_state2info['is_failed'] = str(res['failed'])
                except:
                    dict_state2info['is_failed'] = 'False'
                try:
                    dict_state2info['msg'] = str(res['msg']).strip()
                except:
                    pass
                    
            dict_task2state[str(task_name)] = dict_state2info
            dict_ip2log[str(ip)] = dict_task2state

    return dict_ip2log

    
def playbook_callback_store(pb_json, run_time):
    out_string = pb_json
    filename = '{}.json'.format(run_time)
    out_file = '{webroot}/statics/playbook_log/{filename}'.format(webroot=os.getcwd(),
                                                                  filename=filename)
    with open(out_file, 'w') as f:
        f.write(out_string)
    return out_file 


class PlaybookAPI(tornado.web.RequestHandler):

    def get(self):
        """
        http get method, use in playbook auto run
        """
        task_desc = 'Tianya System Change'
        user = 'Ansible'
        group_id = self.get_argument('group_id')
        run_time = str('%.4f' % time.time())

        # check time, only run in week: 2 or 4, hour: 08:30-09:00
        week = int(time.strftime('%w'))
        hour = int(time.strftime('%H%M'))
        is_exec = False
        if week == 2 or week == 4:
            if hour > 829 or hour < 900:
                # run pb
                is_exec = True

        # execute playbook
        is_exec = True
        if is_exec:

            # get json from callback
            res_json = run_playbook(group_id)
            # get simple dict from callback json
            dict_res = playbook_callback_analysis(res_json)
            # store fully json into a file
            json_uri = playbook_callback_store(res_json, run_time)

            if res_json:
                dict_insert = {'task_desc': task_desc,
                               'user': user,
                               'group_id': group_id,
                               'log_info': str(dict_res).replace('\'', '"'),
                               'log_uri': json_uri,
                               'run_timestamp': run_time}
                insert_res = pb_log.write_table(dict_insert)
                if insert_res:

                    out_string = """<html><head><title>稍候。。。</title></head>
<body>
<script language='javascript'>document.location = '../playbook/log?group_id={}&run_timestamp={}'</script>
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
        dict_args['group_id'] = self.get_argument('group_id')        
        dict_args['run_timestamp'] = self.get_argument('run_timestamp')

        json_str = pb_log.read_table(dict_args)
        json_dict = json.loads(json_str)
        
        out_string = json.dumps(json_dict, indent=4, sort_keys=True)
        # self.write(out_string)

        self.render('playbook_result.html', dict=json_dict)
