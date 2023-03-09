from django.urls import path
from .views import home, pricing

urlpatterns = [
    path('', home, name='home-page'),
    path('ai-content-pricing', pricing, name='pricing'),
]
