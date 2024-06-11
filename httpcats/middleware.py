from django.http import HttpResponseRedirect
from django.shortcuts import redirect

level200 = [i for i in range(200,205)]
level400 = [i for i in range(400,405)] + [409]
level500 = [i for i in range(500,205)] + [599]

class CustomHttpCatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in [level200,level400,level500]:
            # Redirect to the HTTP Cats page for errors
            return redirect('httpcats:http_cat',response.status_code)
        return response

# middleware intercepts all http requests
# # if 404 error, redirect to cats page 
# If it's not a 404 error, we just let the response go through as usual.


# init -sets up the middleware and prepares it to handle requests.