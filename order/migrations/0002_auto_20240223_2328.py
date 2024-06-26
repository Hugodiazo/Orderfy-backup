# Generated by Django 3.2.1 on 2024-02-24 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_auto_20240222_0110'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredientaddeditemorder',
            unique_together={('menu_item_order', 'menu_item_ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='ingredientremoveditemorder',
            unique_together={('menu_item_order', 'menu_item_ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='menuitemorder',
            unique_together={('menu_item', 'order')},
        ),
    ]
