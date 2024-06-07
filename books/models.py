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
