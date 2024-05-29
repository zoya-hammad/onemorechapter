from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(default='1920-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='genre',
            field=models.CharField(default='novel', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
    ]
