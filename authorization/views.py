from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def login(request):
    return render(request, 'authorization/login.html', {})


def register(request):
    return render(request, 'authorization/register.html', {})
