from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.username

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/authors')

    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)

    def deceased(self):
        return self.date_of_death is not None

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}:{self.name}'

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    n_pages = models.IntegerField()
    image = models.ImageField(upload_to='images/books')
    publication_year = models.IntegerField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    

    def __str__(self):
        return f'{self.title} - {self.author}'

    def clean_title(self):
        return self.title.lower().replace(' ', '')


# book page: book title,book author reviews+rating(comments), overall rating, no of pages,add to shelf, author, more books by author(clickable link),

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    n_stars = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.n_stars}'


class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)



class Comment(models.Model):
    text = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



# notes:

# User class: 
# - AbstractUser: you get all the fields and functionalities provided by Django's default user model (username, password, email, etc.)
# - follows: This is a ManyToManyField that allows users to follow each other
# - self': This indicates that the field is a reference to the same model (User). 
#       symmetrical=False: This means the relationship is not necessarily symmetrical. If User A follows User B, it doesn't automatically mean that User B follows User A.
#       related_name='followers': This allows you to access the followers of a user. 
# - related_name='followers': This specifies the name to use for the reverse relation from the User model to itself when accessing the followers of a user. helps access access related objects in a reverse direction.
# - __self__ method: convert the object to a string to to provide a human-readable representation of the model instance.


# Author class: 
# id: set as PK automatically
# images uploaded to the images/authors directory.

# Shelf class: 
# on_delete=models.CASCADE -> means that when a referenced object (book or user) is deleted, then it will also be deleted from the shelfs table 

