from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ClientInfo)
admin.site.register(models.Order)
admin.site.register(models.MenuItemOrder)
admin.site.register(models.IngredientAddedItemOrder)
admin.site.register(models.IngredientRemovedItemOrder)