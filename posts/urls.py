from django.urls import path
from .views import add_comment, delete_post, home_view, create_post, post_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_post, name='create_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('comment/add/<int:post_id>/', add_comment, name='add_comment'),
    path('<int:post_id>/', post_detail_view, name='post_detail'),

]
