from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import os

def home_view(request):
    c = {}
    return render(request, 'pages/home.html', c)

def main_view(request):
    c = {}
    return render(request, 'pages/main.html', c)

def doc_view(request):
    c = {}
    
    if request.method == "POST":        
        uploaded = request.FILES['file']
        target_folder = os.getcwd()+'/src/media/files/'
        
        if uploaded.name not in os.listdir(target_folder):
            with open(target_folder+uploaded.name, 'wb+') as fp:
                for c in uploaded.chunks():
                    fp.write(c)
        
        return redirect('home')
    
    return render(request, 'pages/doc_qa.html', c)

def resume_view(request):
    c = {}
    return render(request, 'pages/resume.html', c)