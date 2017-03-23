#!/usr/bin/env python
# coding:utf-8

import tornado.web
import methods.readdb as mrd


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        # self.write(username)
        user_infos = mrd.select_table(table='users',
                                      column='*',
                                      condition='username',
                                      value=username)
        
        if user_infos:
            db_pwd = user_infos[0][2]

            if db_pwd == password:
                self.write('welcome you: {}'.format(username))
            else:
                self.write('your password was not right')

        else:
            self.write('There is no this user.')


class ArgHandler(tornado.web.RequestHandler):
    def get(self):
        value = self.get_argument('key', 'default_get_value')
        self.write('this is the get value: {}'.format(value))
    def post(self):
        value = self.get_body_argument('key', 'default_post_value')
        self.write('this is the post value: {}'.format(value))
