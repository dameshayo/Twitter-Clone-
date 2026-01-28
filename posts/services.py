from itertools import count
from turtle import title

from users import models
from .models import Post
from django.db.models import Count
from .models import Comment



def get_all_posts():
    return Post.objects.all().order_by('-created_at').prefetch_related('comments')


def get_posts_by_user(user):
    return Post.objects.filter(user=user).order_by('-created_at')

def delete_post(post_id):
    return Post.objects.filter(id=post_id).delete()


def create_post(user, title, content):
    return Post.objects.create(
        user=user,
        title=title,
        content=content
    )

def create_comment(post, user, content):
  
    return Comment.objects.create(
        post=post,
        user=user,
        content=content
    )

def all_comments_for_post(post):
    from .models import Comment
    return Comment.objects.filter(post=post).order_by('-created_at')

def is_post_liked_by_user(post, user):
    from .models import PostLike
    return PostLike.objects.filter(post=post, user=user).exists()

def individual_comments_count(post, user=None):
    from .models import Comment
    qs = Comment.objects.filter(post_id=post.id)

    if user:
        qs = qs.filter(user_id=user.id)

    return qs.count()

def get_comments_count_for_posts(post_ids, user_id=None):
    queryset = Comment.objects.filter(post_id__in=post_ids)

    if user_id:
        queryset = queryset.filter(user_id=user_id)

    queryset = queryset.values('post_id').annotate(
        count=Count('id')
    )

    return {item['post_id']: item['count'] for item in queryset}




