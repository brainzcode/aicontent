from django.urls import path
from .views import home, pricing

urlpatterns = [
    path('', home, name='home-page'),
    path('pricing-ai-content', pricing, name='pricing'),
]
