from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following_profiles',
        blank=True
    )

    def __str__(self):
        return self.user.username

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return Profile.objects.filter(followers=self.user).count()

    class Meta:
        db_table = "profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Follower(models.Model):
    follower_from = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    follower_to = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follower'
        unique_together = ('follower_from', 'follower_to')
        indexes = [
            models.Index(fields=['follower_from']),
            models.Index(fields=['follower_to']),
        ]

    def __str__(self):
        return f"{self.follower_from} follows {self.follower_to}"
  