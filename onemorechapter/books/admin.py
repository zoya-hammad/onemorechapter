from django.contrib import admin 
from .models import Author, Book, Genre, User, Shelf

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Shelf)

# admin.py file is where you can register your models to make them available and manageable through Django's admin interface.
# from django.contrib import admin : provides the admin interface.