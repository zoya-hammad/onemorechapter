from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class CustomHttpCatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            # Redirect to the HTTP Cats page for 404 error
            return redirect('httpcats:http_cat',response.status_code)
        return response

# middleware intercepts all http requests
# # if 404 error, redirect to cats page 
# If it's not a 404 error, we just let the response go through as usual.


# init -sets up the middleware and prepares it to handle requests.