from .models import Genre

def genres_processor(request):
    genres = Genre.objects.all()  
    return {'genres': genres}