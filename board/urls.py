from django.urls import path

from board import views

app_name = "boards"

urlpatterns = [
    path("<int:pk>/",
         views.BoardsView.as_view(), name="boards"),
    path("", views.BoardsView.as_view(), name="boards"),
]
