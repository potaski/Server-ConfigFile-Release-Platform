#!/usr/bin/env python
# coding: utf-8

import tornado.web
import ty_ansible
import os
import datetime
import ConfigParser


class PrintHosts(tornado.web.RequestHandler):

    def get(self):
        hosts_file = '/etc/ansible/hosts'
        modify_time = datetime.datetime.fromtimestamp(int(os.path.getmtime(hosts_file))).strftime('%Y-%m-%d %H:%M:%S')
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read(hosts_file)
        
        
        lst_group_id = config.sections()
        
        for group_id in lst_group_id:
        
            if group_id.lower() == 'test':
                group_info = '测试服务器组'
            else:
                group_info = ty_ansbile.info_switch(method='id2info', data_in=group_id)
                
            my_content = '<p><input type="radio" name="group_id" value="{group_id}"/>  {group_info}  <a href="/hosts?group_id={group_id}">详情</a></p>\n'
            my_content = my_content.format(group_id=group_id, group_info=group_info)

        #self.write(out_html)
        self.render('ansible_host.html', my_content=my_content)