from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from twitter import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]
    
    class Meta:
        db_table = 'post'
