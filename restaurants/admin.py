from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Restaurant)
admin.site.register(models.Branch)
admin.site.register(models.TypeOfCategory)
admin.site.register(models.Category)
admin.site.register(models.MenuItem)

admin.site.register(models.Ingredient)
admin.site.register(models.MenuItemIngredient)