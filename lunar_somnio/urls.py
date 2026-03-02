from django.urls import path
from lunar_somnio import views

app_name = 'lunar_somnio'

urlpatterns = [
    path('', views.index, name='index'),
]