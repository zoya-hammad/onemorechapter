from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def http_cat(request,status_code):
    return render(request, 'cat_status_page.html',{
        "status_code" : status_code,
        'image_url': f'https://http.cat/{status_code}' 
    })