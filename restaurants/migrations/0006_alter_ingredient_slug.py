# Generated by Django 3.2.1 on 2024-02-21 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_auto_20240219_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='slug',
            field=models.SlugField(max_length=20, unique=True),
        ),
    ]