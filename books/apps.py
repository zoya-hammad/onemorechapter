from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

# default_auto_field: specifies the type of auto-generated primary key to use for models in this app (books).
# BigAutoField is a field type in Django that is optimized for large databases. It is a 64-bit integer field. specifies default datatype for PK
# name: Specifies the full Python path to your application. This is how Django identifies and refers to your app internally.
