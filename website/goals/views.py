from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from goals.models import Goal, User

import cjson

def json_response(func):
    def decorated(*args, **kwargs):
        return HttpResponse(cjson.encode(func(*args, **kwargs)), mimetype="application/json")
    return decorated


def goals(request):
    goals = []
    if request.user.is_authenticated():
        goals = request.user.goal_set.order_by('frequency')
    return render_to_response("index.jinja", {"goals": goals, "request": request})

def signup(request):
    context = RequestContext(request)
    if request.method == "GET":
        return render_to_response("signup.jinja", context)

    # Validation.
    email = request.POST.get("email")
    password = request.POST.get("password")
    error = None

    if not ('@' in email or '.' in email):
        error = "Please enter a valid email address."
    elif len(password) < 6:
        error = "Passwords must be at least 6 characters."

    if error:
        context['error'] = error
        return render_to_response("signup.jinja", context)

    # They passed, create the user, log in, and head home.
    user = User.objects.create_user(email, email, password)
    user = authenticate(username=email, password=password)
    login(request, user)
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

