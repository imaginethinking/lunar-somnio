from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Dream, Emotion, WeatherSnapshot, DreamAnalysis
from .models import UserProfile
from django.contrib import messages
from .forms import DreamTitleForm, DreamCreateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
import requests



# 必须加上这个 index 函数，否则服务器启动会崩溃
def index(request):
    if request.method == "POST":
        form = DreamTitleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]

            request.session["dream_title"] = title

            return redirect("lunar_somnio:create_dream")

    else:
        form = DreamTitleForm()

    public_dreams = (
        Dream.objects
        .filter(visibility="public")
        .select_related("user")
        .prefetch_related("emotions")
        .order_by("-created_at")
    )

    context_dict = {
        "form": form,
        "public_dreams": public_dreams,
    }

    return render(request, "lunar_somnio/index.html", context_dict)

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

def logout_view(request):
    logout(request)
    return redirect('lunar_somnio:login')

@login_required
def user_profile(request):
    user = request.user

    user_profile = UserProfile.objects.get(user=user)
    total_dreams = Dream.objects.filter(user=user).count()
    avg_sq = Dream.objects.filter(user=user).aggregate(Avg('sleep_quality'))
    recent_dream = Dream.objects.filter(user=user).order_by('-dreamed_at').first()

    top_month = (Dream.objects.filter(user=user).annotate(month=TruncMonth('dreamed_at')).values('month')
                              .annotate(count=Count('id')).order_by('-count').first())

    top_emotions = (Emotion.objects.filter(dreams__user=user).annotate(count=Count('dreams')).order_by('-count')[:5])

    context_dict = {}
    context_dict['user_profile'] = user_profile
    context_dict['total_dreams'] = total_dreams
    context_dict['avg_sq'] = avg_sq
    context_dict['recent_dream'] = recent_dream
    context_dict['top_month'] = top_month
    context_dict['top_emotions'] = top_emotions

    return render(request, 'lunar_somnio/profile.html', context=context_dict)

@login_required
def dream_analyzer(request, id):

        user = request.user

        dream = Dream.objects.get(id=id,user=user)
        emotions = dream.emotions.all()

        next_dream = Dream.objects.filter(user=user, id=dream.id+1).first()
        prev_dream = Dream.objects.filter(user=user, id=dream.id-1).first()

        try: weather = WeatherSnapshot.objects.get(dream=dream)

        except WeatherSnapshot.DoesNotExist:
            weather = None

        try: dream_analysis = DreamAnalysis.objects.get(dream=dream)

        except DreamAnalysis.DoesNotExist:
            dream_analysis = None

        context_dict = {
            'dream': dream,
            'weather': weather,
            'dream_analysis': dream_analysis,
            'emotions': emotions,
            'next_dream': next_dream,
            'prev_dream': prev_dream,
        }

        return render(request, 'lunar_somnio/dream_analyzer.html', context=context_dict)


@login_required
def create_dream(request):
    title = request.session.get("dream_title")

    form = DreamCreateForm(initial={
        "title": title,
        "visibility": "private",
    })

    return render(request, "lunar_somnio/dream_uploader.html", {"form": form})

@login_required
def upload_dream(request):
    if request.method == "POST":
        form = DreamCreateForm(request.POST)

        if form.is_valid():
            dream = form.save(commit=False)
            dream.user = request.user
            dream.latitude = request.POST.get('latitude')
            dream.longitude = request.POST.get('longitude')
            dream.save()

            response = requests.get('http://api.weatherapi.com/v1/history.json', params={
                'key': 'f68f953a7cf64c22830231541261503',
                'q': f"{dream.latitude},{dream.longitude}",
                'dt': dream.dreamed_at.strftime('%Y-%m-%d')
            })

            data = response.json()
            astro = data['forecast']['forecastday'][0]['astro']
            location_name = data['location']['region'] or data['location']['name']
            WeatherSnapshot.objects.create(
                dream=dream,
                moon_phase=astro['moon_phase'],
                moon_illumination=astro['moon_illumination'],
                location_name=location_name,
            )

            print(data['location'])

            form.save_m2m()

            request.session.pop("dream_title", None)

            return redirect("lunar_somnio:dream_analyzer", id=dream.id)
    else:
        title = request.session.get("dream_title")
        form = DreamCreateForm(initial={"title": title})

    return render(request, "lunar_somnio/dream_uploader.html", {"form": form})

@login_required
def edit_dream(request, id):

    user = request.user
    dream = Dream.objects.get(id=id,user=user)

    if request.method == "POST":
        form = DreamCreateForm(request.POST,instance=dream)

        if form.is_valid():
            dream = form.save(commit=False)
            dream.user = request.user
            dream.save()

            form.save_m2m()

            request.session.pop("dream_title", None)

            return redirect("lunar_somnio:dream_analyzer", id=dream.id)
    else:
        title = request.session.get("dream_title")
        form = DreamCreateForm(instance=dream)

    return render(request, "lunar_somnio/edit_dream.html", {"form": form, "dream": dream})

@login_required
def latest_dream(request):
    dream = Dream.objects.filter(user=request.user).order_by('-created_at').first()
    if dream:
        return redirect('lunar_somnio:dream_analyzer', id=dream.id)
    else:
        return redirect('lunar_somnio:index')