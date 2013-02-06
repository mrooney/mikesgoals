from coffin.shortcuts import render_to_response
from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.contrib import messages
from django.core.validators import email_re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def github(request):
    from django.conf import settings
    import subprocess
    subprocess.check_call(["git", "pull"], cwd=settings.WEBSITE_DIR)
    subprocess.check_call(["python", "deploy.py"], cwd=settings.WEBSITE_DIR)
    return HttpResponse()

def login(request):
    def failure(error_msg):
        return r2r("login.jinja", request, locals())

    if request.method == "GET":
        return r2r("login.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login_user(request, user)
                # Redirect to a success page.
                return redirect("home")
            else:
                # Return a 'disabled account' error message
                return failure("This account has been disabled.")
        else:
            # Return an 'invalid login' error message.
            return failure("Invalid email address or password.")

def logout(request):
    logout_user(request)
    return redirect("home")

def signup(request):
    if request.method == "GET":
        return r2r("signup.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        if not email_re.match(email):
            error_msg = "Please enter a valid email address."
            return r2r("signup.jinja", request, locals())
        if len(password) < 6:
            error_msg = "Please enter a password of at least 6 characters."
            return r2r("signup.jinja", request, locals())
        if User.objects.filter(username=email).count():
            error_msg = "An account with this email address already exists."
            return r2r("signup.jinja", request, locals())

        user = User.objects.create_user(email, password=password)
        user.save()
        user = authenticate(username=email, password=password)
        login_user(request, user)
        return redirect("home")

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

def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None):

    from goals.forms import PasswordResetForm as password_reset_form
    from django.contrib.auth.tokens import default_token_generator as token_generator

    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            form.save(**opts)
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = { 'form': form }
    if extra_context is not None:
        context.update(extra_context)
    return r2r(template_name, request, context)

def password_reset_done(request):
    message = "We've e-mailed you your username and instructions for resetting your password to the e-mail address you submitted. You should be receiving it shortly."
    messages.success(request, message)
    return redirect('home')

