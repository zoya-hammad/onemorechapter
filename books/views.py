from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError

from .models import User, Book, Shelf, Comment

# Create your views here.
def index(request):
    username = request.session.get('username')
    shelf_items = Shelf.objects.filter(user__username=username)
    return render(request, "index.html", {
        'username': username,
        'shelf_items':shelf_items
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
<<<<<<< HEAD
        clean_query = query.lower().replace(' ', '')
        try:
            books = Book.objects.filter(title__icontains=clean_query)
            matching_book = books.first().clean_title()
            return redirect('books:book_page', book_name=matching_book)
        except Book.DoesNotExist:
            return HttpResponse('No book found with that title.')
    return render(request, 'search.html')
=======
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


    

>>>>>>> 9706097969b3044767ce8847e79596d7ad3a2482
