from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    AlbumCreateView,
    PhotoCreateView,
    VideoCreateView,
    PostUpdateView,
    PostDeleteView,
    Favorited_View,
    CategoryPostView,
    CategoryView, CategoryVideoView, PlaylistView, MemeCreateView, CategoryUpdateView, CategoryDeleteView,
    WatchVideoView)
from . import views
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    #path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('playlist/<str:username>/', PlaylistView.as_view(), name='user-playlist'),
    path('album/<str:username>/', CategoryView.as_view(), name='user-category'),
    path('album/<str:name>/photo/', CategoryPostView.as_view(), name='category-posts'),
    path('playlist/<str:name>/video/', CategoryVideoView.as_view(), name='category-videos'),
    path('watch/', WatchVideoView.as_view(), name='watch-videos'),
    path('favorited/<str:username>/post/',Favorited_View.as_view(), name='favorited-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/new/', AlbumCreateView.as_view(), name='album-create'),
    path('post/video/new/', VideoCreateView.as_view(), name='video-create'),
    path('post/photo/new/', PhotoCreateView.as_view(), name='photo-create'),
    path('post/meme/new/', MemeCreateView.as_view(), name='meme-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('album/<int:pk>/update/', CategoryUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', CategoryDeleteView.as_view(), name='album-delete'),

    path('notifications/', views.ShowNOtifications, name='show-notifications'),
    path('notifications/<noti_id>/delete', views.DeleteNotification, name='delete-notification'),

    path('chat', views.Inbox, name='inbox'),
    path('chat/directs/<username>', views.Directs, name='directs'),
    path('chat/delete/', views.DeleteMessage, name='delete'),
    path('chat/new/', views.UserSearch, name='usersearch'),
    path('chat/new/<username>', views.NewConversation, name='newconversation'),
    path('chat/send/', views.SendDirect, name='send_direct'),

    path('post/<int:pk>/comment/', views.add_reply_to_comment, name='add_reply'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('<int:pk>/profile/', views.profile, name='profile_me'),
    path('<int:pk>/fellowship/', views.relations, name='fellowship'),
    path('upload/', views.uploadWhat, name='upload'),
    path('post/<int:pk>/like', views.LikeView, name='like_post'),
    path('post/<int:pk>/like_comment', views.Likecomment, name='like_comment'),
    path('post/<int:pk>/dislike_comment', views.dislikecomment, name='dislike_comment'),
    path('post/<int:pk>/favorite', views.favorite, name='postfavorite')
]
