from django.urls import path

from post.api.v1 import views

app_name = 'post-v1'

urlpatterns = [
    path('create/', views.CreatePostAPIView.as_view(), name='create'),
    path('delete/<int:id>/', views.DestroyPostAPIView.as_view(), name='delete'),
    path(
        'user/<slug:username>/', views.ListUserPostAPIView.as_view(), name='user-list'
    ),
]
