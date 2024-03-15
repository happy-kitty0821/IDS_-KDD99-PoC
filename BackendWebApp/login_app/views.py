from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import sendEmail, getAndStoreIp, scanPorts
from .models import *
# Create your views here.

@login_required(login_url='landing') #this @login required is a decorater that will act as a basic ACS
def homepage(request):
    current_user = request.user
    user_id = current_user.id
    #fetching all the portstatus 
    portStatusValues = PortStatus.objects.all()
    print(f"port status {portStatusValues}")
    print(f"user_id : {user_id}")
    
    contex = {
        'user_id' : user_id,
        'portstatus' : portStatusValues
    }
    return render(request, 'index.html', contex)

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"username is {username} and password is {password} entered by th user")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("<h1> username or password incorrect </h1>")
    #print(f"username : {username}")
    #print(f"password : {password}")
    return render(request, 'login.html')

def landing(request):
    getAndStoreIp()#calling the function from .utls.py
    return render(request, 'landing.html')

def aboutproject(request):
    return render(request, 'aboutproject.html')

@login_required(login_url='landing')
def passwordchange(request):
    return render(request, 'passwordchange.html')

def error404(request, xception):
    return render(request, 'Error404.png', {})


@login_required(login_url='landing')
def register(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        print(uname, passwd1, passwd2, email)
        if passwd1 == passwd2:
            print("passwd1 == passwd2", passwd1 , "and", passwd2)
            password = passwd1
            user = User.objects.create_user(username=uname, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            sendEmail(email, uname, password)
            return redirect('/home')
        else:
            return HttpResponse("<h1>wrong password entered</h1>")
    return render(request, 'register.html')

@login_required(login_url='landing')
def logoutuser(request):
    logout(request)
    return redirect('landing')

@login_required(login_url='landing')
def profile(request):
    return render(request, 'index.html')