from django.db import models
from books.models import User
# Create your models here.

class ChatGptBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_input = models.TextField()
    bot_response = models.TextField()

    def __str__(self):
        return self.user.username