from django.shortcuts import render

def index(request):
    return render(request, 'lunar_somnio/index.html', context={})


