# Generated by Django 4.2.10 on 2024-02-23 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animeSuki', '0012_alter_add_anime_image_alter_add_manga_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_anime',
            name='image',
            field=models.ImageField(upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='add_manga',
            name='image',
            field=models.ImageField(upload_to='static/images'),
        ),
    ]