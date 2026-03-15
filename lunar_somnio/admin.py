from django.contrib import admin
from .models import UserProfile, Dream, Emotion

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Dream)
admin.site.register(Emotion)