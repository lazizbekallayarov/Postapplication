from django.urls import path, include
from .views import (CreatePostAPIView, ListPostAPIView, GetAuthorAPIView, DeletePostsAPIView,
                    DestroyDetailPostAPIView,UpdatePostAPIView)

urlpatterns = [
    path('create_post/', CreatePostAPIView.as_view(), name='post-create'),
    path('get_posts/', ListPostAPIView.as_view(), name='get-posts'),
    path('get_detail_post/<int:pk>', GetAuthorAPIView.as_view(), name='get-detail'),
    path('delete_posts/', DeletePostsAPIView.as_view(), name='delete-posts'),
    path('delete_post_user/<int:pk>/<uuid:uuid>/', DestroyDetailPostAPIView.as_view(), name='delete-posts-user'),
    path('update_post_user/<int:pk>/<uuid:uuid>/', UpdatePostAPIView.as_view(), name='delete-posts-user'),
]