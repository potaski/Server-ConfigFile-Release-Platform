#!/usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
from application import application
from tornado.web import define, options


define('port', default=80, help='run on the given port', type=int)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print 'Development server is running at http://0.0.0.0:{}'.format(options.port)
    print 'Quit the server with Control-C'

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
