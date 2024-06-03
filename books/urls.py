from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('signup/',views.register, name="register"),
    path('books/<str:book_name>/', views.book_page, name="book_page"),
    path('addtoshelf/<int:book_id>/', views.add_to_shelf, name="add_to_shelf"),
    path('removefromshelf/<int:book_id>/', views.remove_from_shelf, name="remove_from_shelf"),
    path('<str:username>/shelf/', views.my_shelf, name='my_shelf'),
    path('add_comment/<int:id>/<str:title>/', views.add_comment, name='add_comment'),
    path('searchbar/', views.search, name="search"),

]
