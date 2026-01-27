from django.urls import path
from .views import delete_post, home_view, create_post

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_post, name='create_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),

]
