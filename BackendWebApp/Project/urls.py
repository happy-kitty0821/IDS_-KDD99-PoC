"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginUser, name = 'login'),
    path('', views.landing, name = 'landing'),
    path('aboutproject/', views.aboutproject, name = 'aboutproject'),
    path('passwordchange/', views.passwordchange, name='passwordchange'),
    # path('passwordchange/otpVerify/', views.otpVerification, name='otpverify'),
    # path('passwordchange/otpVerify/changepass/', views.changePassword, name='changepassword'),
    path('register/', views.register, name='register'),
    path('home', views.homepage, name='home'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('sysinfo/', views.sysInfoTable, name='sysChartTable'),     
    path('sysinfo/jsondata', views.sysinfo, name='systeminfo'),
    path('delete/<int:id>/', views.deleteRecord, name='delete'),     
    path('deleteUser/<int:id>/', views.deleteUser, name='deleteUser'),     
    
    
]

handler404 = 'login_app.views.error404'