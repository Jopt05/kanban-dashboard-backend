from django.urls import path

from auth_app import views

app_name = "user"

urlpatterns = [
    path("register/", views.AuthAppView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login")
]
