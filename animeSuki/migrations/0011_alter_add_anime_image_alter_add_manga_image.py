# Generated by Django 4.2.10 on 2024-02-23 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animeSuki', '0010_add_manga_details_add_manga_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_anime',
            name='image',
            field=models.ImageField(upload_to='NONE'),
        ),
        migrations.AlterField(
            model_name='add_manga',
            name='image',
            field=models.ImageField(upload_to='NONE'),
        ),
    ]
