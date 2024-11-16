from django.shortcuts import render, redirect
from .models import ChatGptBot

from dotenv import load_dotenv
load_dotenv()

from django.contrib import messages
from django.contrib.auth.decorators import login_required

import os
import openai
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key,)

# Create your views here.

custom_prompt = "Please make sure your message is related to books, reading, or journaling. Keep it simple and easy to understand. Avoid NSFW content. Let's talk books!"

from django.http import HttpResponse  # Import HttpResponse for debugging

@login_required
def chatbot(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            #get user input from the form
            user_input = request.POST.get('userInput')
            #clean input from any white spaces
            clean_user_input = str(user_input).strip()
            #send request with user's prompt
            try:
                response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                            {
                                "role": "user",
                                "content": clean_user_input,
                            }
                        ],
                    )
                #get response
                
                bot_response = response.choices[0].message.content
                
                obj, created = ChatGptBot.objects.get_or_create(
                    user=request.user,
                    messageInput=clean_user_input,
                    bot_response=bot_response,
                )
            except openai.APIConnectionError as e:
                #Handle connection error here
                messages.warning(request, f"Failed to connect to OpenAI API, check your internet connection")
            except openai.RateLimitError as e:
                #Handle rate limit error (we recommend using exponential backoff)
                messages.warning(request, f"You exceeded your current quota, please check your plan and billing details.")
                messages.warning(request, f"If you are a developper change the API Key")
                

            return redirect('bookbot:chatbot')
        else:
            #retrieve all messages belong to logged in user
            get_history = ChatGptBot.objects.filter(user=request.user)
            context = {'get_history':get_history}
            return render(request, 'chat.html', context)

def index(request):
    return redirect('bookbot:chatbot')

