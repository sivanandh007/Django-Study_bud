from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('room/<str:ids>/',views.room,name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<int:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<int:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<int:pk>/',views.deleteMessage,name="delete-message")
]
