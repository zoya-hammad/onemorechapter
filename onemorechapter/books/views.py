from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Count

from .models import User, Book, Shelf, Comment, Author, Genre
import random
# Create your views here.

def index(request):
    return redirect('books:home_page')

def home_page(request):
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

# helper functions
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

def get_top_authors(user, limit):
    authors = (
        Shelf.objects.filter(user=user)
        .values('book__author')
        .annotate(count=Count('book__author'))
        .order_by('-count')[:limit]
        )
    return [
        {
        'author': Author.objects.get(id=author['book__author']),
        'count': author['count']
        }
        for author in authors
        ]

def get_top_genres(user, limit):
        genres = (
            Shelf.objects.filter(user=user)
            .values('book__genres')
            .annotate(count=Count('book__genres'))
            .order_by('-count')[:limit]
        )
        return [
            {
                'genre': Genre.objects.get(id=genre['book__genres']),
                'count': genre['count']
            }
            for genre in genres
        ]

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
    
@login_required
def add_to_shelf(request,book_id):
    if request.method == "POST":
        user = request.user
        book = Book.objects.get(id=book_id)
    
        shelf_item = Shelf(user=user, book=book)
        shelf_item.save()

        return redirect('books:book_page', book_name=book.clean_title())

@login_required 
def remove_from_shelf(request,book_id):
    if request.method == "POST":
        user = request.user
        book = Book.objects.get(id=book_id)
        shelf_item = Shelf.objects.get(user=request.user, book_id=book_id)
        shelf_item.delete()

        return redirect('books:book_page', book_name=book.clean_title())

@login_required   
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
    search_query = request.GET.get('search', '')
    if search_query:
        genres = Genre.objects.filter(name__icontains=search_query)
    else:
        genres = Genre.objects.all()

    genres_with_books = []
    for genre in genres:
        books_for_genre = Book.objects.filter(genres=genre)[:3]
        genres_with_books.append({
            'genre': genre,
            'books': books_for_genre
        })

    return render(request, 'genres_list.html', {'genres_with_books': genres_with_books, 'search_query': search_query})


def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books_for_genre = Book.objects.filter(genres=genre)
    return render(request, 'genre_detail.html', {
        'genre': genre,
        'books_for_genre': books_for_genre
    })


'''def search_genre(request):
    if request.method == 'POST':
        query = request.POST.get('search_input')
        clean_query = query.lower().replace(' ', '') 
        all_genre_names = Genre.objects.values_list('name', flat=True)
        exact_match = [name for name in all_genre_names if clean_title(name) == clean_query]
        
        if exact_match:
            # Redirect to the genre detail page if an exact match is found
            genre = Genre.objects.get(name__iexact=exact_match[0])
            return redirect('books:genre_detail', genre_id=genre.id)
            
        else:
            partial_matches = [name for name in all_genre_names if clean_query in clean_title(name)]
            matched_genres = Genre.objects.filter(name__in=partial_matches)
            return render(request, 'genres_list.html', {
                'genres': matched_genres,
                'search_query' : query
            })
    else:
        genres = Genre.objects.all()
        return render(request, 'genres_list.html', {'genres': genres})
     '''

@login_required
def recommended_top_picks(request):
    user = request.user

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

    
@login_required
def user_stats(request):
    user = request.user

    # Get top genres and authors
    top_genres = get_top_genres(user, 3)
    top_authors = get_top_authors(user, 3)

    # Get the most popular book in the user's shelf
    most_popular_book = None
    if user.is_authenticated:
        # Get the list of books shelved by the most users
        most_shelved_books = (
            Shelf.objects.values('book')
            .annotate(num_users=Count('user', distinct=True))
            .order_by('-num_users')
        )
        # Iterate over each book to find the one with the highest number of shelves in the user's shelf
        max_shelves = 0
        for shelved_book in most_shelved_books:
            book = Book.objects.get(id=shelved_book['book'])
            num_shelves = book.shelf_set.filter(user=user).count()
            if num_shelves > max_shelves:
                max_shelves = num_shelves
                most_popular_book = book

        longest_book = None
        if user.is_authenticated:
            shelf_books = Shelf.objects.filter(user=user)
            longest_book = shelf_books.order_by('-book__n_pages').first().book if shelf_books.exists() else None

        shortest_book=None
        if user.is_authenticated:
            shelf2_books = Shelf.objects.filter(user=user)
            shortest_book = shelf2_books.order_by('-book__n_pages').last().book if shelf2_books.exists() else None


    context = {
        'top_genres': top_genres,
        'top_authors': top_authors,
        'most_popular_book': most_popular_book,
        'longest_book': longest_book,
        'shortest_book':shortest_book,
    }

    return render(request, 'user_stats.html', context)




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

