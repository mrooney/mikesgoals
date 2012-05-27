from django.shortcuts import render_to_response

from goals.models import Goal

def goals(request):
    goals = Goal.objects.all()
    return render_to_response("index.jinja", {"goals": goals})

