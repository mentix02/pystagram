from django.urls import path

from user.api.v1 import views

app_name = 'user-v1'

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view(), name='create'),
    path('token/', views.ObtainAuthDataAPIView.as_view(), name='token'),
    path(
        'username-availability/',
        views.UsernameAvailabilityAPIView.as_view(),
        name='username-availability',
    ),
    path(
        'following/<slug:username>/',
        views.UserFollowingAPIView.as_view(),
        name='following',
    ),
    path(
        'followers/<slug:username>/',
        views.UserFollowersAPIView.as_view(),
        name='followers',
    ),
]
