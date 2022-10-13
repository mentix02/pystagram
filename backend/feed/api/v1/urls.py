from django.urls import path

from feed.api.v1 import views

app_name = 'feed-v1'

urlpatterns = [
    path('', views.FeedAPIView.as_view(), name='feed'),
    path('follow/', views.FollowUserAPIView.as_view(), name='follow'),
    path('unfollow/', views.UnfollowUserAPIView.as_view(), name='unfollow'),
]
