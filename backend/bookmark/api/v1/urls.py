from django.urls import path

from bookmark.api.v1 import views

app_name = 'bookmark-v1'

urlpatterns = [
    path('create/', views.CreateBookmarkAPIView.as_view(), name='create'),
    path('list/', views.ListBookmarkedPostsAPIView.as_view(), name='list'),
    path('delete/<int:post_id>/', views.DeleteBookmarkAPIView.as_view(), name='delete'),
]
