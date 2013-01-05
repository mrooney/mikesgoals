# About
mikesgoals is a simple goal-tracking web application, inspired by
joesgoals.com. It cuts out a lot of the features of joesgoals that I
found to add clutter and interaction complexity (goal weight, negative
goals, statistics), while adding the ability to track weekly, monthly,
and yearly goals, besides just daily goals.

It lives at http://goals.rowk.com.

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
1. ./manage.py syncdb --migrate
1. ./deploy.py [starts/restarts application]
