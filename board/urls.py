from django.urls import path

from board import views

app_name = "board"

urlpatterns = [
    path("users/boards/<int:user_id>/", views.BoardsView.as_view(), name="boards"),
]