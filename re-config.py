#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<ACICFG>
# Purpose: Config the config file of lixian.xunlei-Openshift
# Created: 12/10/2014

import sys
import os
import string
import random

#----------------------------------------------------------------------
def main():
    """"""
    # Install requirements
    os.system('pip install -r requirements.txt')
    if os.environ.get('OPENSHIFT_PYTHON_PORT'):
        port = str(os.environ.get('OPENSHIFT_PYTHON_PORT'))
        # python-2.x
    else:
        port = str(os.environ.get('OPENSHIFT_DIY_PORT'))
        # diy-0.1
    if os.environ.get('OPENSHIFT_PYTHON_IP'):
        ip = str(os.environ.get('OPENSHIFT_PYTHON_IP'))
        # python-2.x
    else:
        ip = str(os.environ.get('OPENSHIFT_DIY_IP'))
        # diy-0.1
    cookie_secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(40))
    data_dir = str(os.environ.get('OPENSHIFT_DATA_DIR'))
    repo_dir = str(os.environ.get('OPENSHIFT_REPO_DIR'))
    f = open(repo_dir + 'config.conf', 'w')
    ff = '''username = ""
password = ""
google_client_id = ""
google_client_secret = ""
port = {port}
bind_ip = "{ip}"
ga_account = ""
baidu_account = ""
site_name = u"Thunder Lixian Exporter Openshift"
site_subtitle = u"By Beining@ACICFG"
cookie_secret = "{cookie_secret}"
database_engine = "sqlite:///{data_dir}/task_files.db"
'''.format(port = port, ip = ip, cookie_secret = cookie_secret, data_dir = data_dir)
    ff = ff.encode("utf8")
    f.write(ff)
    f.close()


if __name__=='__main__':
    main()