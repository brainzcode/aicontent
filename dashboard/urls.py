from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='dashboard'),
    path('profile', profile, name='profile'),

    # Blog generation
    path('blog-topic', blogTopic, name='blog-topic'),
    path('blog-section', blogSection, name='blog-section'),

    path('delete-topic/<str:uniqueId>/', deleteBlogTopic, name='delete-topic'),
    path('generate-blog-from-topic/<str:uniqueId>/',
         createBlogFromTopic, name='generate-blog-from-topic'),
    # Save Blog Topic Generated
    path('save-topic/<str:blogTopic>/', saveBlogTopic, name='save-topic'),
    path('use-topic/<str:blogTopic>/', useBlogTopic, name='use-topic'),
    path('view-generated-blog/<slug:slug>/',
         generatedBlog, name='view-generated-blog'),

    # Billing Page
    path('billing/', billing, name='billing'),
]
