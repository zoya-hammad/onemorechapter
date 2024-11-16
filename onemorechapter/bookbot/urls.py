from django.urls import path 
from . import views

app_name = 'bookbot' 

urlpatterns = [
    path('', views.index, name="index"),
    path("chatbot/", views.chatbot, name="chatbot"),
]