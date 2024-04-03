import pyotp
import psutil
from datetime import timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .utils import sendEmail, getAndStoreIp, scanPorts, sendOTPMail
from .models import *
from django.db.models import Q
from django.utils import timezone
# Create your views here.


def sysinfo(request):#this function will get all the information about the ram and cpu usage with 500ms delay
    cpu_percent = psutil.cpu_percent(interval=0.500)
    ram_percent = psutil.virtual_memory().percent
    print(f"cpu usage{cpu_percent}")
    return JsonResponse({'cpu_percent': cpu_percent, 'ram_percent': ram_percent})


@login_required(login_url='landing') #this @login required is a decorater that will act as a basic ACS
def homepage(request):
    current_user = request.user
    user_id = current_user.id
    #fetching all the portstatus from the database
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

def passwordchange(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            userInfo = User.objects.get(username=username)
            userEmail = userInfo.email
            totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
            otp = totp.now()
            validTime = timezone.now() + timedelta(minutes=5)
            sendOTPMail(otp, userEmail)
            print(f"the otp is {otp} and the valid time is {validTime}")
            messages.success(request, "Email sent, check for OTP.")
            # Check if an OTPCode object already exists for the user
            existing_otp = OTPCode.objects.filter(username=userInfo)
            if existing_otp.exists():
                existing_otp = existing_otp.first()
                existing_otp.otpCode = otp
                existing_otp.expireTime = validTime
                existing_otp.save()
            else:
                otpTable = OTPCode.objects.create(username=userInfo, otpCode=otp, isVerified=False, expireTime=validTime)
            return render(request, 'otpVerification.html', {'username': username})
        except ObjectDoesNotExist:
            messages.error(request, f"User '{username}' not found.")
    return render(request, 'passwordchange.html')

def otpVerification(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userOTP = request.POST.get('user_otp')
        print(f"username is {username} and the otpcode is {userOTP}")
        try:
            userInfo = User.objects.get(username=username)
            otpTable = OTPCode.objects.get(username=userInfo)
            if otpTable.isVerified:
                messages.error(request, "OTP has already been verified.")
            elif otpTable.expireTime < datetime.now():
                messages.error(request, "OTP has expired. Please request a new one.")
            elif otpTable.otpCode == userOTP:
                otpTable.isVerified = True
                otpTable.save()
                messages.success(request, "OTP verified successfully. You can now change your password.")
                return render(request, 'changePassword.html', {'username': username})
            else:
                messages.error(request, "Incorrect OTP. Please try again.")
        except ObjectDoesNotExist:
            messages.error(request, f"User '{username}' not found.")
    return render(request, 'otpVerification.html')


def changePassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            userInfo = User.objects.get(username=username)
            userInfo.set_password(new_password)
            userInfo.save()
            messages.success(request, "Password changed successfully.")
            return redirect('login')  # Redirect to login page after password change
    return render(request, 'changePassword.html')



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
    #pw and email change form
    if request.method == "POST":
        currentUsername = request.POST.get('username')
        newEmail = request.POST.get('newEmail')
        currentPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        print(f"username = {currentUsername} newEmail = {newEmail}")
        userRow = User.objects.get(username=currentUsername)#getting the orw which details of the user
        print(f"userow = {userRow}")
         # Check if the current password matches the user's password
        if userRow.check_password(currentPassword):
            # Update user's email
            user.email = newEmail
            user.save()
            # Change password if a new password is provided
            if newPassword:
                user.set_password(newPassword)
                user.save()
            # Display success message
            messages.success(request, 'Profile updated successfully.')
        else:
            # Display error message if current password is incorrect
            messages.error(request, 'Incorrect current password.')

    return render(request, 'profile.html')

def getCpuAndRamUsage(request, *args, **kwargs):
    return JsonResponse()