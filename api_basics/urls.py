from django.urls import path
from .views import SignUp, Login, Logout, TodoDelete, TodoList

urlpatterns = [
    path("register/", SignUp.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("todo/", TodoList.as_view()),
    path("todo/<int:id>/", TodoDelete.as_view())
]
