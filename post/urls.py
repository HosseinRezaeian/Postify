from django.urls import path
from .views import postsView, AddPost, postView, like_ajax_view

urlpatterns = [
    path('posts/', postsView.as_view(), name='posts'),
    path('create/', AddPost.as_view(), name='addpost'),
    path('<str:slug>/', postView.as_view(), name='postview'),
    path('likepost/post', like_ajax_view, name='like_ajax_view'),
]
