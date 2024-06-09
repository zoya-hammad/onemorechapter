from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Count, Q

from .models import User, Book, Shelf, Comment, Author, Genre
import random

# Create your views here.

from django.db.models import Count, Q
import random

def index(request):
    username = request.session.get('username')
    popular_books = Book.objects.annotate(num_shelves=Count('shelf')).order_by('-num_shelves')[:3]

    shelf_items = None
    recommended_books = []
    if request.user.is_authenticated:
        user = request.user
        shelf_items = Shelf.objects.filter(user=user)
        shelf_book_ids = shelf_items.values_list('book_id', flat=True)
        
        # Determine the most read genres
        top_genres = Shelf.objects.filter(user=user).values('book__genres').annotate(count=Count('book__genres')).order_by('-count')
        
        # Determine the top recommended books based on the most read genre
        if top_genres:
            top_genre_id = top_genres[0]['book__genres']
            recommended_books = Book.objects.filter(genres=top_genre_id).exclude(id__in=shelf_book_ids)[:3]

        # If not enough books found, select random books not in shelf
        if len(recommended_books) < 3:
            remaining_books_needed = 3 - len(recommended_books)
            random_books = Book.objects.exclude(id__in=shelf_book_ids).order_by('?')[:remaining_books_needed]
            recommended_books = list(recommended_books) + list(random_books)
        
    return render(request, "index.html", {
        'username': username,
        'shelf_items': shelf_items,
        'popular_books': popular_books,
        'recommended_books': recommended_books
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request,user)
            request.session['username'] = username # storing username in current session
            return HttpResponseRedirect(reverse("books:index"))
        else:
            return render(request, "login.html", {
                "error_message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("books:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not email or not password or not confirmation:
            return render(request, "register.html", {
                "error_message": "All fields are required."
            })
        
        if password != confirmation:
            return render(request, "register.html", {
                "error_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "error_message": "Username already taken."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
def book_page(request, book_name):
    cleaned_book_name = book_name.lower().replace(' ', '')
    
    book = None
    for b in Book.objects.all():
        if b.clean_title() == cleaned_book_name:
            book = b
            break
    
    if not book:
        return HttpResponse("Book not found", status=404)
    
    other_books = Book.objects.filter(author=book.author).exclude(id=book.id)

    in_shelf = False
    if request.user.is_authenticated:
        in_shelf = Shelf.objects.filter(user=request.user, book=book).exists()

    comments = Comment.objects.filter(book=book)

    return render(request,'book_page.html',{
        "book": book,
        "other_books" : other_books,
        "in_shelf" : in_shelf,
        "comments": comments
    })
    
def add_to_shelf(request,book_id):
    if request.method == "POST":
        user = request.user
        book = Book.objects.get(id=book_id)
    
        shelf_item = Shelf(user=user, book=book)
        shelf_item.save()

        return redirect('books:book_page', book_name=book.clean_title())
    
def remove_from_shelf(request,book_id):
    if request.method == "POST":
        user = request.user
        book = Book.objects.get(id=book_id)
        shelf_item = Shelf.objects.get(user=request.user, book_id=book_id)
        shelf_item.delete()

        return redirect('books:book_page', book_name=book.clean_title())
    
def my_shelf(request,username):
    shelf_items = Shelf.objects.filter(user__username=username)
    return render(request,'shelf.html',{
        "username" : username,
        'shelf_items': shelf_items
    })
    #shelf function

@login_required
def add_comment(request, id, title):
    if request.method == "POST":
        comment = request.POST.get('content')
        if comment and id:
            book = Book.objects.get(id=id)
            Comment.objects.create(
                text=comment,
                book=book,
                user=request.user
            )
            return redirect('books:book_page', book_name=book.clean_title())
        else:
            return redirect('books:book_page', book_name=book.clean_title())
        
def clean_title(title):
    return title.lower().replace(' ', '')

def search(request):
    if request.method == 'POST':
        query = request.POST.get('search_input')
        clean_query = query.lower().replace(' ', '') 
        all_titles = Book.objects.values_list('title', flat=True)
        exact_match = [title for title in all_titles if clean_title(title) == clean_query]
        
        if exact_match:
            return redirect('books:book_page', book_name=exact_match[0])
            
        else:
            partial_matches = [title for title in all_titles if clean_query in clean_title(title)]
            return render(request, 'partial_matches.html', {
                'partial_matches': partial_matches,
                'search_query' : query
                }  
            )
    else:
        return render(request, 'search.html')

def authors_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        authors = Author.objects.filter(author_name__icontains=search_query)
    else:
        authors = Author.objects.all()
    return render(request, 'authors_list.html', {'authors': authors, 'search_query': search_query})

def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    books_by_author = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {
        'author': author,
        'books_by_author': books_by_author
    })

def genres_list(request):
    genres = Genre.objects.all()
    genres_with_books = []
    for genre in genres:
        books_for_genre = Book.objects.filter(genres=genre)[:3]
        genres_with_books.append({
            'genre': genre,
            'books': books_for_genre
        })
    return render(request, 'genres_list.html', {'genres_with_books': genres_with_books})

'''
def genre_detail(request, genre_id):
    genre= Genre.objects.get(id=genre_id)
    books_for_genre= Book.objects.filter(genre=genre)
    return render(request, 'genre_detail.html',{
        'genre':genre,
        'books_for_genre':books_for_genre

    }) '''

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books_for_genre = Book.objects.filter(genres=genre)
    return render(request, 'genre_detail.html', {
        'genre': genre,
        'books_for_genre': books_for_genre
    })


@login_required
def recommended_top_picks(request):
    user = request.user

    # Helper functions to get top genres and author
    def get_user_top_genre(user, rank):
        genres = Shelf.objects.filter(user=user).values('book__genres').annotate(count=Count('book__genres')).order_by('-count')
        if rank <= len(genres):
            return Genre.objects.get(id=genres[rank-1]['book__genres'])
        return None

    def get_user_top_author(user):
        authors = Shelf.objects.filter(user=user).values('book__author').annotate(count=Count('book__author')).order_by('-count')
        if authors:
            return Author.objects.get(id=authors[0]['book__author'])
        return None

    def get_books_not_in_shelf(user, genre=None, author=None):
        shelf_book_ids = Shelf.objects.filter(user=user).values_list('book_id', flat=True)
        if genre:
            return Book.objects.filter(genres=genre).exclude(id__in=shelf_book_ids)[:6]
        if author:
            return Book.objects.filter(author=author).exclude(id__in=shelf_book_ids)[:6]
        return Book.objects.exclude(id__in=shelf_book_ids)[:6]

    # Get user's top genres and author
    top_genre1 = get_user_top_genre(user, 1)
    top_genre2 = get_user_top_genre(user, 2)
    top_author = get_user_top_author(user)

    # Get books for the genres and author excluding those in the user's shelf
    top_genre1_books = get_books_not_in_shelf(user, genre=top_genre1)
    top_genre2_books = get_books_not_in_shelf(user, genre=top_genre2)
    top_author_books = get_books_not_in_shelf(user, author=top_author)

    context = {
        'top_genre1': top_genre1,
        'top_genre2': top_genre2,
        'top_genre1_books': top_genre1_books,
        'top_genre2_books': top_genre2_books,
        'top_author': top_author,
        'top_author_books': top_author_books,
    }
    return render(request, 'recommended_top_picks.html', context)


    
# import render: Renders a template with a given context.
# When you call render, Django takes the specified template, fills it with the data from the context, and returns the complete HTML page as an HttpResponse.

# redirect: Redirects to another URL.
# reverse: Resolves URL names to actual URLs.
# authenticate: Verifies a user's credentials. (login, logout etc)
# HttpResponse is used to send content back to the client.
# HttpResponseRedirect is a subclass of HttpResponse specifically used for redirecting the client to a different URL. 
# IntegrityError: Exception raised for database integrity issues


# def index(request): func that takes a http request (acc to a particular url)

# in the login view: if request.method == "POST": indicates that the form has been submitted 

# cleaned_book_name: makes it easier to match books by conv to lowercase and removing spaces 

