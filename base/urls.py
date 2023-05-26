from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("room/<str:pk>/", views.room, name="room"),
    path("login/", views.authPage, name="authPage"),
    path("register/", views.registerUser, name="Register"),
    path("logout/", views.logoutPage, name="Logout"),

    path("create_room/", views.create_room, name="create_room"),

    path("profile/<str:pk>/", views.userProfile, name="user_Profile"),


    path("delete_room/<str:pk>/", views.delete_room, name="delete_room"),

    path("update_room/<str:pk>/", views.Update_room, name="update_room"),
    path("delete_message/<str:pk>/", views.delete_msg, name="delete_msg"),

    path("update_user/", views.update_user, name="update_user"),


    path("topic/", views.topic_page, name="topic_page"),


    path("activity/", views.activity_page, name="activity_page"),

]
