from django import views
from django.urls import path
from .views import follow_view, register_view, login_view, profile_view, logout_view, unfollow_view

urlpatterns = [
    path('', login_view, name='login'),  # Redirect root to login for simplicity
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),

    path('follow/<int:user_id>/', follow_view, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_view, name='unfollow'),
]
