from django.shortcuts import render_to_response
from django.http import HttpResponse
from goals.models import Goal

import cjson

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated


def goals(request):
    goals = []
    if request.user.is_authenticated():
        goals = request.user.goal_set.all()
    return render_to_response("index.jinja", {"goals": goals, "request": request})

@json_response
def api_check(request):
    goal_id = request.GET['id']
    goal_date = request.GET['date']
    action = request.GET['action']

    return {'success': True}

