from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import re

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def login(request):
    c = {}
    if request.POST:
        email = request.POST["email"]
        password = request.POST["pass"]

        if email and password and re.match(r"[^@]+@[^@]+\.[^@]+", email):
            user = User.objects.create_user(
                username=email.split("@")[0], email=email, password=password
            )
            user.save()
            response = {"status": 1, "url": "/dash/", "msg": "Success"}
        else:
            response = {"status": 0, "url": "", "msg": "Error"}
        return HttpResponse(json.dumps(response), content_type="application/json")

    return render(request, "pages/login.html", c)


def dashboard(request):
    c = {}
    return render(request, "pages/dash.html", c)
