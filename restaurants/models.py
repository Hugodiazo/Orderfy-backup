from django.db import models
from . import functions

# Create your models here.
class Restaurant(models.Model):   
    def get_upload_to_path_logo(self, filename):
        return f'{self.slug}/logo/{filename}'
    def get_upload_to_path_image(self, filename):
        return f'{self.slug}/image/{filename}'

    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=80)
    slug= models.SlugField(max_length=20, unique=True)
    description= models.TextField(max_length=1000, blank=True, null=True)
    logo= models.ImageField(upload_to=get_upload_to_path_logo, default="default_restaurant_logo.png")
    image= models.ImageField(upload_to=get_upload_to_path_image, default="default_restaurant_image.png")
    primary_color= models.CharField(max_length=7, validators=[functions.validate_color_hex])
    secondary_color= models.CharField(max_length=7, validators=[functions.validate_color_hex])
    q_branches= models.PositiveSmallIntegerField(default=1, validators=[functions.validate_not_zero])

    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name=  "Restaurant"
        verbose_name_plural= "Restaurants"
    
class Branch(models.Model):
    def get_upload_to_path_image(self, filename):
        return f'{self.restaurant.slug}/image/{self.slug}/{filename}'

    restaurant= models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length= 100)
    ubication= models.CharField(max_length= 200, default='unknown')
    slug= models.SlugField(max_length=20, unique=True)
    image= models.ImageField(upload_to=get_upload_to_path_image, default= "default_branch.png")

    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name=  "Branch"
        verbose_name_plural= "Branches"

class TypeOfCategory(models.Model):
    def get_upload_to_path_image(self, filename):
        return f'{self.branch.restaurant.slug}/image/{self.branch.slug}/{self.slug}/{filename}'

    branch= models.ForeignKey(Branch, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length= 100)
    slug= models.SlugField(max_length=20, unique=True)
    image= models.ImageField(upload_to=get_upload_to_path_image, default= "default_type_of_category.avif")

    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name=  "Type of category"
        verbose_name_plural= "Types of categories"

    def __str__(self):
        return self.name

class Category(models.Model):
    type_of_category= models.ForeignKey(TypeOfCategory, on_delete=models.CASCADE)

    id = models.AutoField(primary_key= True)
    name= models.CharField(max_length=80)
    slug= models.SlugField(max_length=20, unique=True)
    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name=  "Category"
        verbose_name_plural= "Categories"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_upload_to_path_image(self, filename):
        return f'{self.category.type_of_category.branch.restaurant.slug}/image/{self.category.type_of_category.branch.slug}/{self.category.type_of_category.slug}/{self.category.slug}/{filename}'

    id = models.AutoField(primary_key= True)
    name= models.CharField(max_length=80)
    description= models.TextField(max_length=1000, blank=True, null=True)
    image= models.ImageField(upload_to=get_upload_to_path_image, default= 'default_menu_item.jpg')
    price= models.DecimalField(max_digits= 10, decimal_places= 2)
    in_stock= models.BooleanField(default= True)
    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name=  "Menu Item"
        verbose_name_plural= "Menu Items"

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    menuItem= models.ManyToManyField(MenuItem, related_name="Ingredient", through='MenuItemIngredient')
    restaurant= models.ForeignKey(Restaurant, on_delete= models.CASCADE)

    def get_upload_to_path_image(self, filename):
        return f'{self.restaurant.slug}/image/ingredients/{filename}'

    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length= 80)
    slug= models.SlugField(max_length= 20, unique=True)
    in_stock= models.BooleanField(default= True)
    image= models.ImageField(upload_to= get_upload_to_path_image, default= 'default_ingredient.png')
    created= models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name=  "Ingredient"
        verbose_name_plural= "Ingredients"

    def __str__(self):
        return self.name
    
class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    removable = models.BooleanField(default=True) 
    price_remove = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    addable= models.BooleanField(default=False)
    price_add = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('menu_item', 'ingredient')
        verbose_name=  "Menu Item Ingredient"
        verbose_name_plural= "Menu Item Ingredients"

    def __str__(self):
        return self.menu_item.name + " " + self.ingredient.name
    


