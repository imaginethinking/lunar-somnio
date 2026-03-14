# from django.urls import path
# from lunar_somnio import views

# app_name = 'lunar_somnio'

# urlpatterns = [
#     path('', views.index, name='index'),
# ]
from django.urls import path
from . import views

app_name = 'lunar_somnio'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('login/', views.login_view, name='login'),      # 网址：/lunar_somnio/login/
    path('register/', views.register_view, name='register'), # 网址：/lunar_somnio/register/
    path("dream/create/", views.create_dream, name='create_dream'),
    path("dream/upload/", views.upload_dream, name='upload_dream'),
    path('profile/', views.user_profile, name='profile'),
    path('dream/<int:id>', views.dream_analyzer, name='dream_analyzer'),
]