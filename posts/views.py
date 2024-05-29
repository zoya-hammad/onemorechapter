from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from books.models import User
from .models import Post

# Create your views here.
def post_feed(request,username):
    user = User.objects.get(username=username)
    followed_users = user.follows.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    return render(request, 'post_feed.html', 
        {'posts': posts, 
         'user': user}
    )

def new_post(request,username):
    return render(request, 'new_post.html', {'username': username})


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
    
def post_page(request,id):
    post = Post.objects.get(id=id)
    return render(request, 'post_page.html',{
            "post" : post
        })
    