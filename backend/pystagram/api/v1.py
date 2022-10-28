from django.urls import path, include

urlpatterns = [
    path('user/', include('user.api.v1.urls')),
    path('post/', include('post.api.v1.urls')),
    path('like/', include('like.api.v1.urls')),
    path('feed/', include('feed.api.v1.urls')),
    path('story/', include('story.api.v1.urls')),
    path('comment/', include('comment.api.v1.urls')),
    path('bookmark/', include('bookmark.api.v1.urls')),
]
