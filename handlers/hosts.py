#!/usr/bin/env python
# coding: utf-8

import tornado.web
import ty_ansible
import os
import datetime
import ConfigParser


class HostGroup(tornado.web.RequestHandler):

    def get(self):
        hosts_file = '/etc/ansible/hosts'
        modify_time = datetime.datetime.fromtimestamp(int(os.path.getmtime(hosts_file))).strftime('%Y-%m-%d %H:%M:%S')
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read(hosts_file)
        
        count_line = 0
        submit_icon = '<input type="submit" value="Run Playbook" style="height:30px;width:120px;" />'
        lst_group_id = config.sections()
        
        for group_id in lst_group_id:
            count_line += 1
        
            if group_id.lower() == 'test':
                group_info = '测试服务器组'
            else:
                group_info = ty_ansbile.info_switch(method='id2info', data_in=group_id)
                
            out_string = '<p><input type="radio" name="group_id" value="{group_id}"/>  {group_info}  <a href="/hosts?group_id={group_id}">查看IP列表</a></p>\n'
            out_string = out_string.format(group_id=group_id, group_info=group_info)
            
            if str(count_line)[-1] == '9':
                out_string = out_string + '\n' + submit_icon

        #self.write(out_html)
        self.render('ansible_host.html', my_content=out_string)
        
        
class HostGroupIPs(tornado.web.RequestHandler):
    
    def get(self):
        group_id = self.get_argument('group_id')
        ansible_host = ty_ansible.AnsibleHost()
        lst_ip = ansible_host.get_group_lstip(group_id)
        
        out_string = ''
        for ip in lst_ip:
            out_string = out_string + '{}<br>\n'.format(ip)
        
        self.write(out_string)