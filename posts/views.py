from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from posts.forms import CommentForm
from posts.forms import CommentForm
from posts.models import Post
from . import services

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


@login_required
def home_view(request,post_ids=None):
    
    posts = services.get_all_posts()

    # post_ids = posts.values_list('id', flat=True)

    comments_count = services.get_comments_count_for_posts(post_ids) if post_ids else 0
    following_ids = set(
        request.user.following
        .values_list('follower_to_id', flat=True)
    )
    return render(request, 'posts/home.html', {'posts': posts, 'following_ids': following_ids, 'comments_count': comments_count})

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


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

    return redirect('home')  # or redirect to profile/post detail

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comments = services.all_comments_for_post(post)

    context = {
        'post': post,
        'comments': comments,
        'comments_count': comments.count(),
    }
    return render(request, 'posts/post_detail.html', context)
