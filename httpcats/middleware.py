from django.http import HttpResponseRedirect
from django.shortcuts import redirect

level100 = [i for i in range(100,104)]
level200 = [i for i in range(200,209)] + [214,226]
level300 = [i for i in range(300,306)] + [307,308]
level400 = [i for i in range(400,419)] + [i for i in range(420,427)] + [428,429,431,444,450,451,497,498,499,]
level500 = [i for i in range(500,512)] + [522,522,523,525,530,599]

class CustomHttpCatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in [level100,level200,level300,level400,level500]:
            # Redirect to the HTTP Cats page for errors
            return redirect('httpcats:http_cat',response.status_code)
        return response

# middleware intercepts all http requests
# # if 404 error, redirect to cats page 
# If it's not a 404 error, we just let the response go through as usual.


# init -sets up the middleware and prepares it to handle requests.