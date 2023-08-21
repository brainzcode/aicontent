from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'ai/index.html', {})


def pricing(request):
    return render(request, 'ai/pricing.html', {})
