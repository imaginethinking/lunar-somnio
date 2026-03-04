from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

# 必须加上这个 index 函数，否则服务器启动会崩溃
def index(request):
    return render(request, 'lunar_somnio/index.html')

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        user = authenticate(request, username=uname, password=pword)
        if user:
            login(request, user)
            return redirect('lunar_somnio:index') 
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'lunar_somnio/login.html')

def register_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pword = request.POST.get('password')
        age = request.POST.get('age')
        
        # 创建账号并关联 Profile
        user = User.objects.create_user(username=uname, email=email, password=pword)
        UserProfile.objects.create(user=user, age=age, display_name=uname)
        return redirect('lunar_somnio:login')
    return render(request, 'lunar_somnio/register.html')