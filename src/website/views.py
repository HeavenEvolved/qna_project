from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import os

def login(request):
    c = {}
    return render(request, 'pages/login.html', c)