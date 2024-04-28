# Generated by Django 3.2.1 on 2024-02-13 20:57

from django.db import migrations, models
import django.db.models.deletion
import restaurants.functions
import restaurants.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('ubication', models.CharField(default='unknown', max_length=200)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('image', models.ImageField(default='default_branch.png', upload_to=restaurants.models.Branch.get_upload_to_path_image)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('logo', models.ImageField(default='default_restaurant_logo.png', upload_to=restaurants.models.Restaurant.get_upload_to_path_logo)),
                ('image', models.ImageField(default='default_restaurant_image.png', upload_to=restaurants.models.Restaurant.get_upload_to_path_image)),
                ('primary_color', models.CharField(max_length=7, validators=[restaurants.functions.validate_color_hex])),
                ('secondary_color', models.CharField(max_length=7, validators=[restaurants.functions.validate_color_hex])),
                ('q_branches', models.PositiveSmallIntegerField(default=1, validators=[restaurants.functions.validate_not_zero])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='TypeOfCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('image', models.ImageField(default='default_branch.png', upload_to=restaurants.models.TypeOfCategory.get_upload_to_path_image)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.branch')),
            ],
            options={
                'verbose_name': 'Type of category',
                'verbose_name_plural': 'Types of categories',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(upload_to=restaurants.models.MenuItem.get_upload_to_path_image)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('in_stock', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.category')),
            ],
            options={
                'verbose_name': 'Menu Item',
                'verbose_name_plural': 'Menu Items',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='type_of_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.typeofcategory'),
        ),
        migrations.AddField(
            model_name='branch',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
