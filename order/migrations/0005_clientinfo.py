# Generated by Django 5.0.3 on 2024-03-19 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_menuitemorder_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('gmail', models.EmailField(max_length=254)),
                ('age', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ClientInfo', to='order.order')),
            ],
            options={
                'verbose_name': 'Client Information',
                'verbose_name_plural': 'Clients Information',
            },
        ),
    ]
