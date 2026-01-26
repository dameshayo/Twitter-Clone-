from .models import Post


def get_all_posts():
    return Post.objects.all().order_by('-created_at')


def create_post(user, content):
    return Post.objects.create(
        user=user,
        content=content
    )
