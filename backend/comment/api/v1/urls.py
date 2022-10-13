from django.urls import path

from comment.api.v1 import views

app_name = 'comment-v1'

urlpatterns = [
    path('create/', views.CreateCommentAPIView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteCommentAPIView.as_view(), name='delete'),
    path('list/<int:post_id>/', views.ListPostCommentAPIView.as_view(), name='list'),
]
