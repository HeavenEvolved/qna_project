from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import os

def home_view(request):
    c = {}
    return render(request, 'pages/home.html', c)

def login_view(request):
    c = {}
    return render(request, 'pages/login.html')

def register_view(request):
    c = {}
    return render(request, 'pages/register.html')

def reset_view(request):
    c = {}
    
    if request.method == 'POST':
        print(request)
        return redirect('login');
    
    return render(request, 'pages/reset.html')

def main_view(request):
    c = {}
    return render(request, 'pages/main.html', c)

def doc_view(request):
    c = {
        'dropmsg': "Drag-n-Drop or Click to upload your files!"
    }
    
    if request.method == "POST":
        try:
            uploaded = request.FILES['file']
            target_folder = os.getcwd()+'/src/media/files/'
            
            try:
                if uploaded and uploaded.name not in os.listdir(target_folder):
                    with open(target_folder+uploaded.name, 'wb+') as fp:
                        for c in uploaded.chunks():
                            fp.write(c)
                c['dropmsg'] = 'Successfully Uploaded!'
            except:
                c['dropmsg'] = 'Upload Failed!'
        except:
            pass
    
    return render(request, 'pages/doc_qa.html', c)

def resume_view(request):
    c = {
        'dropmsg': "Drag-n-Drop or Click to upload your files!"
    }
    
    if request.method == "POST":
        pass
    
    
    return render(request, 'pages/resume.html', c)