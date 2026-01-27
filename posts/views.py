from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Post
from . import services

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


@login_required
def home_view(request):
    posts = services.get_all_posts()

    following_ids = set(
        request.user.following
        .values_list('follower_to_id', flat=True)
    )
    return render(request, 'posts/home.html', {'posts': posts, 'following_ids': following_ids})

def user_posts_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts_by_user = services.get_posts_by_user(user)
    return render(request, 'posts/user_posts.html', {'posts': posts_by_user, 'profile_user': user})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get('content')
        services.create_post(request.user, title, content)
        return redirect('home')

    return render(request, 'posts/create_post.html')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 🔒 Allow only owner
    if post.user != request.user:
        return redirect('home')

    post = services.delete_post(post_id)
    return redirect('profile' , permanent=True)
