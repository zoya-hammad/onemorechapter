from django.urls import path
from . import views

app_name = 'httpcats' 

urlpatterns= [
    path('<int:status_code>/', views.http_cat, name="http_cat"),
]