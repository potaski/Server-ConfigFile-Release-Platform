#!/usr/bin/env python
# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.index import *
from handlers.ansible import * 

url = [(r'/', IndexHandler),
       (r'/argtest', ArgHandler),
       (r'/api/playbook', PlaybookAPI),
       (r'/ansible/log', QueryPlaybookResult),
      ]
