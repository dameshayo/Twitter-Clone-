from turtle import title
from .models import Post


def get_all_posts():
    return Post.objects.all().order_by('-created_at')


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
