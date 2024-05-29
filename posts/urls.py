from django.urls import path
from . import views

app_name = "posts"

urlpatterns =[
    path('post_feed/<str:username>/', views.post_feed, name='post_feed'),
    path('<str:username>/newpost/',views.new_post, name='new_post'),
    path('submit/', views.submit_post, name='submit_post'),
    path('post/<int:id>/', views.post_page, name='post_page')

]