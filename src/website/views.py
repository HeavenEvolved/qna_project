from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import json
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

User = get_user_model()
# def delete(request):
#     User.objects.all().delete()


def login(request):
    c = {}
    request.session["is_auth"] = False
    if request.POST:
        email = request.POST["u_email"]
        password = request.POST["u_pass"]
        if email and password and re.match(r"[^@]+@[^@]+\.[^@]+", email):
            user = User.objects.get(email=email).check_password(password)
            print(user)
            if user:
                auth_login(request, User.objects.get(email=email))
                response = {
                    "status": 1,
                    "email": email,
                    "url": "dash",
                    "msg": "Success",
                }
                request.session["is_auth"] = True
            else:
                response = {
                    "status": 0,
                    "url": "login",
                    "msg": "User does not Exist",
                }
        else:
            response = {
                "status": 0,
                "url": "login",
                "msg": "Invalid Email or Password",
            }
        request.session["data"] = response
        return redirect(reverse(response["url"]))
    return render(request, "pages/login.html", c)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect(reverse)


def dashboard(request):
    c = {}
    if request.session["is_auth"]:
        return render(request, "pages/dash.html", c)


def data_manage(request):
    c = {}
    return render(request, "pages/data_manage.html", c)
