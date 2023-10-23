from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

def home_view(request):
    return render(request, 'pages/home.html')

def main_view(request):
    return render(request, 'pages/main.html')

@csrf_protect
def doc_view(request):
    c = {}
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        print(files)
        return render(request, 'pages/doc_qa.html', RequestContext(request))
        
    return render(request, 'pages/doc_qa.html', c)

@csrf_protect
def resume_view(request):
    c = {}    
    return render(request, 'pages/resume.html', c)