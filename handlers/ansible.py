#!/usr/bin/env python
# coding:utf-8

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManage
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import tornado.web
import os


class OptionsDefault(object):

    def __init__(self):
        self.connection = 'smart'
        self.check = False
        self.become = True

    def __getattr__(self, name):
        return None


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'json'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        self.results = []

    def _new_play(self, play):
        return {
            'play': {
                'name': play.name,
                'id': str(play._uuid)
            },
            'tasks': []
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.name,
                'id': str(task._uuid)
            },
            'hosts': {}
        }

    def v2_playbook_on_play_start(self, play):
        self.results.append(self._new_play(play))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.results[-1]['tasks'].append(self._new_task(task))

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        self.results[-1]['tasks'][-1]['hosts'][host.name] = result._result

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        output = {
            'plays': self.results,
            'stats': summary
        }

        # print(json.dumps(output, indent=4, sort_keys=True))
        self.res_all = output
        self.res_stats = {'stats': summary}

    def ty_stdout_all(self):
        return self.res_all

    def ty_stdout_stats(self):
        return self.res_stats

    v2_runner_on_failed = v2_runner_on_ok
    v2_runner_on_unreachable = v2_runner_on_ok
    v2_runner_on_skipped = v2_runner_on_ok


class AnsiblePlaybook(tornado.web.RequestHandler):
    
    def get(self):
        try:
            group_id = self.get_argument('group_id')
            playbook = '/etc/ansible/ansible_playbook/{}.yml'.format(group_id)
            if os.path.isfile(playbook):
                ssh_user = 'root'
                ssh_passwd = 'zijicaiba'
                
                loader = DataLoader()
                variable_manager = VariableManager()
                inventory = Inventory(loader=loader, variable_manager=variable_manager)
                variable_manager.set_inventory(inventory)
                callback = CallbackModule()
                options = OptionsDefault()
                variable_manager.extra_vars = {'ansible_ssh_user': ssh_user,
                                               'ansible_ssh_pass': ssh_passwd,
                                               'ansible_become_method': 'sudo',
                                               'ansible_become_user': 'root',
                                               'ansible_become_pass': ssh_passwd}
