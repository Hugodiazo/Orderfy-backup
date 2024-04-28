from django.db import models
from restaurants import models as Rmodels

# Create your models here.

class ClientInfo(models.Model):
    id= models.AutoField(primary_key=True)

    name= models.CharField(max_length= 100)
    email= models.EmailField()
    age= models.PositiveSmallIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=  "Client Information"
        verbose_name_plural= "Clients Information"

    def __str__(self):
        return str(self.name)
    
class Order(models.Model):
    id= models.AutoField(primary_key=True)
    order_id= models.PositiveSmallIntegerField(unique=True)
    client= models.ForeignKey(ClientInfo, related_name='Order', on_delete=models.CASCADE)
    menu_items= models.ManyToManyField(Rmodels.MenuItem, related_name="Order", through='MenuItemOrder')
    branch= models.ForeignKey(Rmodels.Branch, related_name="Order", on_delete= models.CASCADE)
    ordered_from= models.IntegerField(default=0)
    paid= models.BooleanField(default=False)
    delivered= models.BooleanField(default=False)
    pay_later= models.BooleanField(default=True)
    decision_made= models.BooleanField(default= False)
    waiting_waiter= models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=  "Order"
        verbose_name_plural= "Orders"

    def __str__(self):
        return str(self.id) + " / " + str(self.order_id)

class MenuItemOrder(models.Model):
    menu_item = models.ForeignKey(Rmodels.MenuItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    observation = models.CharField(max_length= 150, blank=True, null=True)
    ingredients_added= models.ManyToManyField(Rmodels.MenuItemIngredient, related_name= 'MenuItemOrderAdded', through='IngredientAddedItemOrder')
    ingredients_removed= models.ManyToManyField(Rmodels.MenuItemIngredient, related_name= 'MenuItemOrderRemoved', through='IngredientRemovedItemOrder')

    class Meta:
        verbose_name=  "Menu Item in an order"
        verbose_name_plural= "Menu Items in an order"

    def __str__(self):
        return f'{self.menu_item.name} added to order {self.order.id}'

class IngredientAddedItemOrder(models.Model):
    menu_item_order= models.ForeignKey(MenuItemOrder, on_delete=models.CASCADE)
    menu_item_ingredient= models.ForeignKey(Rmodels.MenuItemIngredient, on_delete=models.CASCADE)
    quantity= models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('menu_item_order', 'menu_item_ingredient')
        verbose_name=  "Ingredient added to menu item in an order"
        verbose_name_plural= "Ingredients added to menu item in an order"

    def __str__(self):
        return f'{self.menu_item_ingredient.ingredient.name} added to {self.menu_item_order.menu_item.name} in order {self.menu_item_order.order.id}'

class IngredientRemovedItemOrder(models.Model):
    menu_item_order= models.ForeignKey(MenuItemOrder, on_delete=models.CASCADE)
    menu_item_ingredient= models.ForeignKey(Rmodels.MenuItemIngredient, on_delete=models.CASCADE)
    quantity= models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('menu_item_order', 'menu_item_ingredient')
        verbose_name=  "Ingredient removed from menu item in an order"
        verbose_name_plural= "Ingredients removed from menu item in an order"

    def __str__(self):
        return f'{self.menu_item_ingredient.ingredient.name} removed from {self.menu_item_order.menu_item.name} in order {self.menu_item_order.order.id}'


