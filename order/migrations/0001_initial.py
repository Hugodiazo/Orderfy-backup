# Generated by Django 3.2.1 on 2024-02-24 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurants', '0007_auto_20240222_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientAddedItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('menu_item_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitemingredient')),
            ],
            options={
                'verbose_name': 'Ingredient added to menu item in an order',
                'verbose_name_plural': 'Ingredients added to menu item in an order',
            },
        ),
        migrations.CreateModel(
            name='IngredientRemovedItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('menu_item_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitemingredient')),
            ],
            options={
                'verbose_name': 'Ingredient removed from menu item in an order',
                'verbose_name_plural': 'Ingredients removed from menu item in an order',
            },
        ),
        migrations.CreateModel(
            name='MenuItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('ingredients_added', models.ManyToManyField(related_name='MenuItemOrderAdded', through='order.IngredientAddedItemOrder', to='restaurants.MenuItemIngredient')),
                ('ingredients_removed', models.ManyToManyField(related_name='MenuItemOrderRemoved', through='order.IngredientRemovedItemOrder', to='restaurants.MenuItemIngredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menuitem')),
            ],
            options={
                'verbose_name': 'Menu Item in an order',
                'verbose_name_plural': 'Menu Items in an order',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ordered_from', models.IntegerField(default=0)),
                ('paid', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='restaurants.branch')),
                ('menu_items', models.ManyToManyField(related_name='Order', through='order.MenuItemOrder', to='restaurants.MenuItem')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AddField(
            model_name='menuitemorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
        migrations.AddField(
            model_name='ingredientremoveditemorder',
            name='menu_item_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.menuitemorder'),
        ),
        migrations.AddField(
            model_name='ingredientaddeditemorder',
            name='menu_item_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.menuitemorder'),
        ),
    ]
