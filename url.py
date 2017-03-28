#!/usr/bin/env python
# coding:utf-8

import tornado.web
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.index import *
from handlers.ansible import * 


url = [(r'/', IndexHandler),
       (r'/argtest', ArgHandler),
       (r'/playbook/api', PlaybookAPI),
       (r'/playbook/log', QueryPlaybookResult),
      ]
