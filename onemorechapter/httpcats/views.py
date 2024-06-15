from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def http_cat(request,status_code):
    return render(request, 'cat_status_page.html',{
        "status_code" : status_code,
        'image_url': f'https://http.cat/{status_code}' 
    # The line `level400 = [i for i in range(400,405)] + [409497,498,499,]` is creating a list called
    # `level400` that contains numbers from 400 to 404 (inclusive) using a list comprehension `[i for i in
    # range(400,405)]`, and then it appends additional numbers 409497, 498, and 499 to the list.
    })