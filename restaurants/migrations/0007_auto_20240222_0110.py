# Generated by Django 3.2.1 on 2024-02-22 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_alter_ingredient_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='MenuItem',
            new_name='menuItem',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='Restaurant',
            new_name='restaurant',
        ),
    ]