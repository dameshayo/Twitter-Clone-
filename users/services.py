from django.db import IntegrityError

from posts.models import Post
from .models import Follower


def follow_user(follower_from, follower_to):
    if follower_from == follower_to:
        raise ValueError("You cannot follow yourself")

    try:
        return Follower.objects.create(
            follower_from=follower_from,
            follower_to=follower_to
        )
    except IntegrityError:
        # Already following
        return None


def unfollow_user(follower_from, follower_to):
    return Follower.objects.filter(
        follower_from=follower_from,
        follower_to=follower_to
    ).delete()


def get_followers(user):
    return Follower.objects.filter(follower_to=user).select_related('follower_from')


def get_following(user):
    return Follower.objects.filter(follower_from=user).select_related('follower_to')


def is_following(user_from, user_to):
    return Follower.objects.filter(
        follower_from=user_from,
        follower_to=user_to
    ).exists()

def get_followers_count(user):
    return Follower.objects.filter(follower_from=user).count()

def get_posts_by_user(user):
    return Post.objects.filter(user=user).order_by('-created_at')

def get_following_count(user):
    return Follower.objects.filter(follower_to=user).count()


def get_user_profile(user):
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=user)
    return profile
