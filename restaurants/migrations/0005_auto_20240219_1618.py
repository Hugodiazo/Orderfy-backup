# Generated by Django 3.2.1 on 2024-02-19 19:18

from django.db import migrations, models
import django.db.models.deletion
import restaurants.models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_alter_typeofcategory_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=20)),
                ('image', models.ImageField(default='default_ingredient.png', upload_to=restaurants.models.Ingredient.get_upload_to_path_image)),
                ('in_stock', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='MenuItemIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removable', models.BooleanField(default=True)),
                ('price_remove', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('addable', models.BooleanField(default=False)),
                ('price_add', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.ingredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitem')),
            ],
            options={
                'verbose_name': 'Menu Item Ingredient',
                'verbose_name_plural': 'Menu Item Ingredients',
                'unique_together': {('menu_item', 'ingredient')},
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='MenuItem',
            field=models.ManyToManyField(related_name='Ingredient', through='restaurants.MenuItemIngredient', to='restaurants.MenuItem'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='Restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
