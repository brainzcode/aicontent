from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='dashboard'),
    path('profile', profile, name='profile'),
]
