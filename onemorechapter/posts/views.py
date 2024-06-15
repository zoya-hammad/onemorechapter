from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from books.models import User
from .models import Post, PostComment

# Create your views here.
@login_required
def post_feed(request,username):
    user = User.objects.get(username=username)
    followed_users = user.follows.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    return render(request, 'post_feed.html', 
        {'posts': posts, 
         'user': user}
    )

@login_required
def new_post(request,username):
    return render(request, 'new_post.html', {'username': username})

@login_required
def submit_post(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image') if 'image' in request.FILES else None
        

        post = Post.objects.create(user=user, title=title, text=text, image=image)
        post.save()
        return render(request, 'post_page.html',{
            "post" : post
        })
    else:
        return render(request, 'new_post.html')

@login_required   
def post_page(request,id):
    post = Post.objects.get(id=id)
    user = request.user
    is_following = False
    if user.is_authenticated:
        is_following = user.user_follows(post.user)

    comments = PostComment.objects.filter(post=post)

    return render(request, 'post_page.html',{
            "post" : post,
            'is_following' : is_following,
            "comments": comments
        })

@login_required    
def more_posts(request, username):
    user = User.objects.get(username=username)
    followed_users = user.follows.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')
    return render(request, 'more_posts.html', {
        'posts': posts,
        'user': user
    })

@login_required
def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'all_posts.html', {'posts': posts})

@login_required
def follow(request,user_id):
    user_to_follow = User.objects.get(pk=user_id)
    request.user.follows.add(user_to_follow)
    messages.success(request, f"You followed {user_to_follow.username} successfully.")
    post_id = request.POST.get('post_id')
    return redirect('posts:post_page',id=post_id )

@login_required
def unfollow(request,user_id):
    user_to_unfollow = User.objects.get(pk=user_id)
    request.user.follows.remove(user_to_unfollow)
    post_id = request.POST.get('post_id')
    return redirect('posts:post_page',id=post_id )

@login_required
def add_comment(request, id, title):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        comment = request.POST.get('content')
        if comment and id:
            PostComment.objects.create(
                text = comment,
                post = post,
                user = request.user
            )
            return redirect('posts:post_page', id=post.id)
        else:
            return redirect('posts:post_page', id=post.id)