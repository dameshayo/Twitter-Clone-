from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services


@login_required
def home_view(request):
    posts = services.get_all_posts()

    following_ids = set(
        request.user.following
        .values_list('follower_to_id', flat=True)
    )
    return render(request, 'posts/home.html', {'posts': posts, 'following_ids': following_ids})


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        services.create_post(request.user, content)
        return redirect('home')

    return render(request, 'posts/create_post.html')
