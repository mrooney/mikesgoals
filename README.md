Pre-requisites:
===============
* Python
* Pip (easy_install pip)
* Redis
* [Optional] virtualenv (pip install virtualenv)

Installation:
=============

From the directory of the repository:
#.[Optional] virtualenv --no-site-packages ve && source ve/bin/activate
#.pip install -r requirements.txt
# website/manage.py syncdb
# website/manage.py migrate goals
# website/manage.py supervisor
