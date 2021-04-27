from django.shortcuts import render

from django.contrib.auth.models import User

def welcomePage(request):
    users = User.objects.all().order_by("username")
    context = {"users":users}
    return render(request, "index.html", context)