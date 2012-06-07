# Pre-requisites:
* python
* pip
 * sudo easy_install pip
* redis
 * OSX: brew install redis
 * Ubuntu: sudo apt-get install redis-server
* [optional] virtualenv
 * pip install virtualenv

# Installation:

From the directory of the repository:

1. [optional] virtualenv --no-site-packages env && source env/bin/activate
1. pip install -r requirements.txt
1. cd website
1. ./manage.py syncdb
1. ./manage.py migrate goals
1. ./manage.py supervisor
