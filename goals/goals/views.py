from django.shortcuts import render_to_response
from django.http import HttpResponse
from goals.models import Goal

import cjson

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated


def goals(request):
    goals = Goal.objects.all()
    return render_to_response("index.jinja", {"goals": goals})

@json_response
def api_check(request):
    name = request.GET['name']
    date = request.GET['date']
    action = request.GET['action']

    return {'success': True, 'date': date, 'name': name, 'action': action}

