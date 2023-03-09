from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.


def login(request):
    return render(request, 'authorization/login.html', {})


def register(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print('Username submitted was: {}'.format(email))

        return redirect('register')
    return render(request, 'authorization/register.html', {})
