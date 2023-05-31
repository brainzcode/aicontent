from django.urls import path
from .views import home, pricing

urlpatterns = [
    path('', home, name='home'),
    path('ai-content-pricing', pricing, name='pricing'),
]
