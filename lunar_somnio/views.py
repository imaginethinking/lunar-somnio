from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Dream, Emotion, WeatherSnapshot, DreamAnalysis, Reaction
from django.contrib import messages
from .forms import DreamTitleForm, DreamCreateForm, UserForm, UserProfileForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
import requests


# Renders the home page, handles quick dream title submission, and fetches public dreams with reactions
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
        .prefetch_related("emotions", "reactions")
        .order_by("-created_at")
    )

    for dream in public_dreams:
        dream.heart_count = dream.reactions.filter(emoji="heart").count()
        dream.laugh_count = dream.reactions.filter(emoji="laugh").count()
        dream.surprised_count = dream.reactions.filter(emoji="surprised").count()
        dream.sad_count = dream.reactions.filter(emoji="sad").count()
        dream.fire_count = dream.reactions.filter(emoji="fire").count()

        if request.user.is_authenticated:
            user_reactions = set(
                dream.reactions.filter(user=request.user).values_list("emoji", flat=True)
            )
            dream.user_reacted = user_reactions
        else:
            dream.user_reacted = set()

    context_dict = {
        "form": form,
        "public_dreams": public_dreams,
    }

    return render(request, "lunar_somnio/index.html", context_dict)


# Handles user authentication and login functionality
def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            uname = login_form.cleaned_data.get('username')
            pword = login_form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pword)
            if user:
                login(request, user)
                return redirect('lunar_somnio:index') 
            else:
                messages.error(request, "Invalid username or password.")
    else:
        # Initialize a blank form for GET requests
        login_form = UserLoginForm()
        
    return render(request, 'lunar_somnio/login.html', {'login_form': login_form})


# Handles new user registration, creating both User and UserProfile records
def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database securely
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            # Save the user profile data to the database
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, 'Account successfully created! You can now log in.')
            return redirect('lunar_somnio:login')
        else:
            messages.error(request, 'Registration failed. Please check your inputs.')
            
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'lunar_somnio/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Logs out the current user and redirects to the login page
def logout_view(request):
    logout(request)
    return redirect('lunar_somnio:login')


# Displays user statistics, recent dreams, and top emotions
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


# Displays detailed analysis, weather data, and emotions for a specific dream
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


# Renders the form to create a new dream entry
@login_required
def create_dream(request):
    title = request.session.get("dream_title")

    form = DreamCreateForm(initial={
        "title": title,
        "visibility": "private",
    })

    return render(request, "lunar_somnio/dream_uploader.html", {"form": form})


# Processes new dream submissions and fetches external weather data
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


# Handles AJAX requests for adding or removing emoji reactions on public dreams
@login_required
def react_to_dream(request, dream_id):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    dream = get_object_or_404(Dream, id=dream_id, visibility="public")
    emoji = request.POST.get("emoji")

    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        dream=dream,
        emoji=emoji
    )

    if not created:
        reaction.delete()

    count = Reaction.objects.filter(dream=dream, emoji=emoji).count()
    reacted = Reaction.objects.filter(
        dream=dream,
        user=request.user,
        emoji=emoji
    ).exists()

    return JsonResponse({
        "success": True,
        "emoji": emoji,
        "count": count,
        "reacted": reacted,
    })


# Allows users to modify their existing dream entries
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


# Redirects the user to their most recently logged dream
@login_required
def latest_dream(request):
    dream = Dream.objects.filter(user=request.user).order_by('-created_at').first()
    if dream:
        return redirect('lunar_somnio:dream_analyzer', id=dream.id)
    else:
        messages.info(request, "You haven't recorded any dreams yet!")
        return redirect('lunar_somnio:index')