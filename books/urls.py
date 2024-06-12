from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.index, name="index"),
    path("onemorechapter/", views.home_page, name="home_page"),
    path("onemorechapter/login", views.login_view, name="login"),
    path("onemorechapter/logout", views.logout_view, name="logout"),
    path('onemorechapter/signup/',views.register, name="register"),
    path('onemorechapter/books/<str:book_name>/', views.book_page, name="book_page"),
    path('onemorechapter/addtoshelf/<int:book_id>/', views.add_to_shelf, name="add_to_shelf"),
    path('onemorechapter/removefromshelf/<int:book_id>/', views.remove_from_shelf, name="remove_from_shelf"),
    path('onemorechapter/<str:username>/shelf/', views.my_shelf, name='my_shelf'),
    path('onemorechapter/add_comment/<int:id>/<str:title>/', views.add_comment, name='add_comment'),
    path('onemorechapter/searchbar/', views.search, name="search"),
    path('onemorechapter/authors/', views.authors_list, name='authors_list'),
    path('onemorechapter/authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('onemorechapter/genres/',views.genres_list,name='genres_list'),
    #path('genres/', views.search_genre, name='genres_list'),
    path('onemorechapter/genres/<int:genre_id>/' ,views.genre_detail,name='genre_detail'),
    path('onemorechapter/recommended_top_picks/', views.recommended_top_picks, name='recommended_top_picks'),  
    path('onemorechapter/user-stats/', views.user_stats, name='user_stats'),
]


# app_name = "books" so that there are no conflicts (incase of multiple apps)

    # index: 
    #User Request: A user makes a request to the root URL of the "books" app.
    #URL Routing: Django checks urls.py and finds that the root URL should be handled by the index view.
    #View Processing: The index view in views.py retrieves the username from the session, queries the database for the user's shelf items, and prepares a context dictionary.
    #Template Rendering: The index view calls render, passing the request, template name (index.html), and context. Django processes the template, inserting the context data into the placeholders.
    #Response: Django returns the rendered HTML page to the user's browser.
