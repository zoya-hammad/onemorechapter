# Generated by Django 5.0.4 on 2024-05-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_genre_book_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]