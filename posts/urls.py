from django.urls import path
from .views import home_view, create_post

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_post, name='create_post'),
]
