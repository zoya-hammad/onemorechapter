from django.db import models
from books.models import User  

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    text = models.TextField()  
    image = models.ImageField(upload_to='images/posts', null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.id} by {self.user.username}'
    

class PostComment(models.Model):
    text = models.CharField(max_length=256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
