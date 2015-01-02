#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
while True:
    s1,m1 = commands.getstatusoutput('/usr/bin/python /var/www/blog/manage.py yinxiang_articles')
    #print('articles status:{}\narticles message:\n{}'.format(s1,m1))
    s2,m2 = commands.getstatusoutput('/usr/bin/python /var/www/blog/manage.py yinxiang_shares')
    #print('shares status:{}\nshares message:\n{}'.format(s2,m2))
    s3,m3 = commands.getstatusoutput('/usr/bin/python /var/www/blog/manage.py yinxiang_home')
    #print('home status:{}\nhome message:\n{}'.format(s3,m3))
    s4,m4 = commands.getstatusoutput('/usr/bin/python /var/www/blog/manage.py up_down_load_resources')
    #print('resources status:{}\n resources message:\n{}'.format(s4,m4))

    with open('/var/log/blog/sync.log', 'a') as f:
        f.write(m1 + '\n')
        f.write(m2 + '\n')
        f.write(m3 + '\n')
        f.write(m4 + '\n')

    time.sleep(15 * 60)
