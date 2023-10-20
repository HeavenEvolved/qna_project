from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(response):
    return HttpResponse("<h1>This is the Login Page!</h1>")

def home(response):
    return HttpResponse("<h1>This is the Home Page!</h1>")

def main(response):
    return HttpResponse("<h1>This is the Main Page!</h1>")