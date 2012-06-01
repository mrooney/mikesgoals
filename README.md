Pre-requisites:
===============
* python
* pip
* redis
* [Optional] virtualenv

OSX: brew install redis
Ubuntu: apt-get install redis-server
finally: easy_install pip && pip install virtualenv

Installation:
=============

From the directory of the repository:
#.[Optional] virtualenv --no-site-packages ve && source ve/bin/activate
#.pip install -r requirements.txt
# website/manage.py syncdb
# website/manage.py migrate goals
# website/manage.py supervisor
