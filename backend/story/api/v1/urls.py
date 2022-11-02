from django.urls import path

from story.api.v1 import views

app_name = 'story-v1'

urlpatterns = [
    path('create/', views.CreateStoryAPIView.as_view(), name='create'),
    path(
        'active-story-following/',
        views.ListFollowingWithActiveStories.as_view(),
        name='active-story-following',
    ),
    path(
        'list/<slug:username>/active/',
        views.ListUserActiveStoriesAPIView.as_view(),
        name='list-active',
    ),
]
