from django.urls import path
from . import views

app_name = "posts"

urlpatterns =[
    path('post_feed/<str:username>/', views.post_feed, name='post_feed'),
    path('<str:username>/newpost/',views.new_post, name='new_post'),
    path('submit/', views.submit_post, name='submit_post'),
    path('post/<int:id>/', views.post_page, name='post_page'),
    path('more_posts/<str:username>/', views.more_posts, name='more_posts'),
    path('all_posts/', views.all_posts, name='all_posts')
    
]

# Example Workflow
# User navigates to /posts/post_feed/johndoe/:

# URL pattern matches path('post_feed/<str:username>/', views.post_feed, name='post_feed').
# Django calls views.post_feed(request, 'johndoe').
# post_feed view retrieves johndoe's followed users and their posts, then renders post_feed.html with this data.