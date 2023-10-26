from django.shortcuts import render , redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from user.models import Project
from django.contrib import messages
from django.contrib.auth import authenticate , login

# def login_view(request):
#     return render(request, 'pages/login.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request,'Invalid Username')
            return redirect('login')
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.info(request,'Invalid Password')
            return redirect('login')
        
        else: 
            login(request,user)
            return redirect('main')

    return render(request,'pages/login.html')

def register_view(request):

    if request.method == "POST":
        
        email = request.POST.get('company_name')
        first_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(email,first_name,username,password)

        user = User.objects.filter(username = username)    
        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('/register')
        
        user = User.objects.create(
            email = email,
            first_name = first_name,
            username = username,
        )

        user.set_password(password)
        user.save()
        messages.success(request, "Account created succesfully")


        return redirect('login')
    
    return render(request, 'pages/register.html')

def forgot_view(request):
    return render(request, 'pages/forgot_pass.html')


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