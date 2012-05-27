from django.http import HttpResponse

from goals.models import Goal

def goals(request):
    response = """<html><head><title>Mike's Goals</title></head><body>%s</body></html>"""
    content = ",".join([goal.name for goal in Goal.objects.all()])

    return HttpResponse(response % content)

