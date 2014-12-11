LiXian.XunLei: api of lixian.xunlei.com in python
=================================================

LiXian.XunLei is a python api base on http://lixian.xunlei.com/ , and a web project using this api.

迅雷离线API是基于迅雷离线网页版开发的python接口，并在这个接口基础上实现一套离线资源分享网站。

Now avalable on Openshift.


Features
--------
Api for lixian.xunlei.com.
 - Including add/fetch/delete/delay tasks or files.
 - Normal/bt/thunder/magnet url support and automatically distinguish.
 - Ulimit offline space.
 - task may expired when you change account or it's nolonger in your tasklist

A website
 - Multi-user with permission control support.
 - Async
 - Search
 - Tags
 - Share
 - Download with wget/aria2

A plugin for flexget
 - add task by flexget
 - get all files as input from xunlei lixian

Installation of Dependencies
----------------------------

First thing first, go to https://developers.google.com/accounts/docs/OAuth2 and register for OAuth2. 

You can deploy a ```diy-0.1``` or ```python-2.x``` of your node.

After the node is deployed and for some reason the config file failed, please log in the shell, edit and run:

::

    python re-config.py

This file is located at ```$OPENSHIFT_REPO_DIR``` .

If requirements fail, please run:

::

    pip install -r requirements.txt

Usage
-----

Edit ```config.conf```, and put your Thunder account and Google OAuth2 info in it.

Then ::

    tmux
    python main.py

If you hate tmux and are sure that you would not need to enter the verify code:

    nohup ${OPENSHIFT_REPO_DIR}/diy/main.py > ${OPENSHIFT_DIY_LOG_DIR}/lixian.xunlei.log 2>&1 &

Getting help ::

    python main.py --help

FlexGet Plugin
--------------
::

    cp libs/jsfunctionParser.py libs/lixian_api.py libs/plugin_lixian_xunlei.py ~/.flexget/plugins/

and add config ::

    xunlei_lixian:
        username: "<your username>"
        password: "<your password>"

presets<http://flexget.com/wiki/Plugins/preset> may help if you want to add it to all feeds.

Requires
--------
::

    2.6 <= python < 3.0


License
-------
Like the upper stream, lixian.xunlei-openshift is licensed under GNU Lesser General Public License.
You may get a copy of the GNU Lesser General Public License from <http://www.gnu.org/licenses/lgpl.txt>

FAQ
-------

1. Why you don't use the built-in start?

    Chances are you will need to enter a verifycode when you login. So I would rather bring it out than ganbling that you would not need to enter any verifycode.
    
    Since you need to enter the user info by yourself, the deploy script is unfinished.
   
   
2. I cannot bind to the internal port! (Usually 8080)
    
    Sometimes Openshift automatically runs a httpd server that would occupy this port, or maybe you did not exit the programme correctly.
    
    Check the environment varible $OPENSHIFT_PYTHON_PORT(or $OPENSHIFT_DIY_PORT if you are using diy). This port is usually 8080.
    Then run:
    
        lsof -i:8080
    
    This will give you all the threads that is occupying this port. 
    
    Kill them with:
    
        kill -9 (pid)
    
    And you should be able to run.

3. How can I make someone admin?
    
    Right now there's no user control panel for this programme, but you can always change the user group to ```admin``` to fix this.
    
    Also you can login with 127.0.0.1.