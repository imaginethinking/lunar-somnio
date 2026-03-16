from django.urls import path
from . import views

app_name = 'lunar_somnio'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path("dream/create/", views.create_dream, name='create_dream'),
    path("dream/upload/", views.upload_dream, name='upload_dream'),
    path('profile/', views.user_profile, name='profile'),
    path('dream/<int:id>', views.dream_analyzer, name='dream_analyzer'),
    path('dream/edit/<int:id>', views.edit_dream, name='edit_dream'),
    path('dream/latest/', views.latest_dream, name='latest_dream'),
]