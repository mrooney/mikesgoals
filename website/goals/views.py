from django.contrib.auth.decorators import user_passes_test
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from goals.models import Goal, User

import cjson

def r2r(template, request, data=None):
    if data is None:
        data = {}
    data['request'] = request
    return render_to_response(template, data, context_instance=RequestContext(request))

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated


def goals(request):
    goals = []
    if request.user.is_authenticated():
        goals = request.user.goal_set.order_by('frequency')
    return r2r("index.jinja", request, {"goals": goals})

def totals(request):
    totals = []
    if request.user.is_authenticated():
        r = Goal().redis
        pipe = r.pipeline()
        for k in r.keys():
            pipe.get(k)
        totals = [{'date': k, 'count': c} for k in r.keys() for c in pipe.execute()]
    return r2r("totals.jinja",request,{'totals':totals})

def github(request):
    from django.conf import settings
    import subprocess
    pid = open(settings.PROJECT_PATH+"/../run/gunicorn.pid").read().strip()
    subprocess.check_call(["git", "pull"], cwd=settings.PROJECT_PATH)
    subprocess.check_call(["kill", "-s", "SIGHUP", pid], cwd=settings.PROJECT_PATH)
    return HttpResponse()

def logout(request):
    auth.logout(request)
    return redirect("/")

def signup(request):
    if request.method == "GET":
        return r2r("signup.jinja", request)

    # Validation.
    email = request.POST.get("email")
    password = request.POST.get("password")
    error = None

    if not ('@' in email or '.' in email):
        error = "Please enter a valid email address."
    elif len(password) < 6:
        error = "Passwords must be at least 6 characters."

    if error:
        return r2r("signup.jinja", request, {'error': error})

    # They passed, create the user, log in, and head home.
    user = User.objects.create_user(email, email, password)
    user = auth.authenticate(username=email, password=password)
    auth.login(request, user)
    return redirect("/")

@json_response
def api_goal_delete(request):
    goal_id = int(request.GET['goal'])

    if not Goal.objects.filter(id=goal_id, user__id=request.user.id).count():
        raise Exception("401 Unauthorized")

    Goal.objects.filter(id=goal_id).delete()
    return {}

@json_response
def api_goal_edit(request):
    goal_id = int(request.GET['goal'])
    goal_name = request.GET['name']

    if not Goal.objects.filter(id=goal_id, user__id=request.user.id).count():
        raise Exception("401 Unauthorized")

    Goal.objects.filter(id=goal_id).update(name=goal_name)
    return {}

@json_response
def api_goal_new(request):
    goal_name = request.GET['name']
    goal_freq = request.GET['frequency']

    Goal(name=goal_name, frequency=goal_freq, user=request.user).save()
    return {}

@json_response
def api_check(request):
    goal_id = request.GET['id']
    goal_date = request.GET['date']
    action = request.GET['action']

    if not Goal.objects.filter(id=goal_id, user__id=request.user.id).count():
        raise Exception("401 Unauthorized")

    incr = 1 if action == "increment" else -1
    Goal.objects.get(id=goal_id).incr(goal_date, incr)
    return {}

