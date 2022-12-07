from django.urls import path

from like.api.v1 import views

app_name = "like-v1"

urlpatterns = [
    path("create/", views.CreateLikeAPIView.as_view(), name="create"),
    path("delete/", views.DeleteLikeAPIView.as_view(), name="delete"),
]
