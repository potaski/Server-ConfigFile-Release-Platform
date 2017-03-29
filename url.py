#!/usr/bin/env python
# coding:utf-8

import tornado.web
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.index import *
from handlers.ansible import *
from handlers.hosts import *


url = [(r'/', PrintHosts),
       (r'/argtest', ArgHandler),
       (r'/playbook/run', RunPlaybook),
       (r'/playbook/log', QueryPlaybookResult),
       (r'/hosts/all', PrintHosts),
      ]
