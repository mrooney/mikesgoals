from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response

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
def api_goal_edit(request):
    goal_id = int(request.GET['goal'])
    goal_name = request.GET['name']

    if not Goal.objects.filter(id=goal_id, user__id=request.user.id).count():
        raise Exception("401 Unauthorized")

    Goal.objects.filter(id=goal_id).update(name=goal_name)

    return {'success': True}

@json_response
def api_check(request):
    goal_id = request.GET['id']
    goal_date = request.GET['date']
    action = request.GET['action']

    if not Goal.objects.filter(id=goal_id, user__id=request.user.id).count():
        raise Exception("401 Unauthorized")

    incr = 1 if action == "increment" else -1
    Goal.objects.get(id=goal_id).incr(goal_date, incr)

    return {'success': True}

