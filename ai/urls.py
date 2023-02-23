from django.urls import path
from .views import home, about

urlpatterns = [
    path('', home, name='home-page'),
    path('about-ai-content', about, name='about-page'),
]
