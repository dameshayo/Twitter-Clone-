from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from . import services
from users.forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Profile

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # If you still want to create a Profile automatically:
            # Profile.objects.create(user=user)
            login(request, user)  # Log the user in immediately
            return redirect('home')  # Redirect to home page after registration
        print(form.errors)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})
    

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get the validated user
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect after successful login
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def profile_view(request):
    profile = services.get_user_profile(request.user)
    
    user_posts = services.get_posts_by_user(request.user)

    followers_count = services.get_followers_count(request.user)
    following_count = services.get_following_count(request.user)

    if request.method == 'POST':
        profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
        profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
        profile.user.save()

        profile.bio = request.POST.get('bio', profile.bio)
        profile.save()
        return redirect('profile')

    return render(request, 'auth/profile.html', {
        'profile_user': profile.user,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts': user_posts
    })


@login_required
def follow_view(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    services.follow_user(request.user, user_to_follow)
    return redirect('home')


@login_required
def unfollow_view(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    services.unfollow_user(request.user, user_to_unfollow)
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')
