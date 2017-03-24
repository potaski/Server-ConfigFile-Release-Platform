create table playbook_log (
id int not null auto_increment,
task_desc varchar(100) not null,
user varchar(30) not null,
group_id varchar(50) not null,
all_log blob not null,
run_timestamp varchar(30) not null,
log_time timestamp not null default current_timestamp,
primary key (id));


# coding:utf-8

"""
Author zhangwei@staff.tianya.cn
File pb_json.py
Create: 2017/3/24 10:24
"""

import json

string = open('pb3.json').read()
string = string.split('.retry\n')[-1]

# store this string into ansible.playbook_log

j = json.loads(string)

aa = j['plays']
ab = aa[0]['tasks']

ba = j['stats']
dict_out = {}

for tmp in ab:
    task_name = tmp['task']['name']

    if tmp['task']['name'] == '':
        print '---FACTER_STATE'
        facter_result = tmp['hosts']

        for ip, res in facter_result.items():
            try:
                is_unreachable = res['unreachable']
                print '  Host: {}'.format(ip)
                print '    Is_Changed: {}'.format(res['changed'])
                print '    Is_Unreachable: {}'.format(res['unreachable'])
                print '    Msg: {}'.format(res['msg'].strip())
            except:
                continue

    else:
        print '---TASKI_STATE'
        print 'Task: {}'.format(task_name)
        task_results = tmp['hosts']

        # task result
        for ip, res in task_results.items():
            print '  Host: {}'.format(ip)
            try:
                print '    Is_Skipped: {}'.format(res['results'][0]['skipped'])
            except:
                print '    Is_Skipped: False'
            print '    Is_Changed: {}'.format(res['changed'])
            try:
                print '    Is_Failed: {}'.format(res['failed'])
            except:
                print '    Is_Failed: False'
            try:
                print '    Msg: {}'.format(res['msg'])
            except:
                pass
                # print json.dumps(res, indent=4, sort_keys=True)

# total result (include facter)
for ip, res in ba.items():
    out = ''
    for desc, num in res.items():
        info = '{}:{} '.format(desc, num)
        out = out + info

    dict_out[ip] = out

print '---TOTAL'
for k,v in dict_out.items():
    print '{} {}'.format(k, v)

