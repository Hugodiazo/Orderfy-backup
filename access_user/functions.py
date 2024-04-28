from django.core.exceptions import ObjectDoesNotExist
from restaurants import models as Rmodels
from .models import CustomUser
import imghdr
import re

def check_user(request, restaurant):
    # Chequea que el usuario pueda acceder a la pagina
    if not request.user.is_superuser:
        users= CustomUser.objects.filter(restaurant=restaurant)
        if request.user not in users: return "no_access" 
        return None

# GETTERS
def get_restaurant(restaurant_slug):
    try:
        restaurant= Rmodels.Restaurant.objects.get(slug= restaurant_slug)
        return restaurant
    except ObjectDoesNotExist:
        return None

def get_branch(branch_slug):
    try:
        branch= Rmodels.Branch.objects.get(slug= branch_slug)
        return branch
    except ObjectDoesNotExist:
        return None

def get_type(type_slug):
    try:
        type_of_category= Rmodels.TypeOfCategory.objects.get(slug= type_slug)
        return type_of_category
    except ObjectDoesNotExist:
        return None

def get_category(category_slug):
    try:
        category= Rmodels.Category.objects.get(slug= category_slug)
        return category
    except ObjectDoesNotExist:
        return None

def get_menu_item(item_id):
    try:
        menu_item= Rmodels.MenuItem.objects.get(id=item_id)
        return menu_item
    except ObjectDoesNotExist:
        return None

def get_menu_items(type_of_category):
    # Devuelve un diccionario que contiene en la key la categoria y en el value todos los menu_items relacionados
    categories= Rmodels.Category.objects.filter(type_of_category= type_of_category)

    menu_items= {}
    for category in categories:
        i= Rmodels.MenuItem.objects.filter(category= category)
        menu_items[category]= i

    return menu_items

def get_ingredient(ingredient_slug):
    try:
        ingredient= Rmodels.Ingredient.objects.get(slug= ingredient_slug)
        return ingredient
    except ObjectDoesNotExist:
        return None

def get_item_ingredient(item, ingredient):
    try:
        item_ingredient= Rmodels.MenuItemIngredient.objects.get(menu_item= item, ingredient= ingredient)
        return item_ingredient
    except ObjectDoesNotExist:
        return None

def get_user(username):
    try:
        user= CustomUser.objects.get(username= username)
        return user
    except ObjectDoesNotExist:
        return None

# VALIDATORS
def is_image(file):
    # Chequea que el archivo sea una imagen
    image_content = file.read()
    file.seek(0) 
    image_type = imghdr.what(None, image_content)
    return image_type is not None

def validate_color_hex(value):
    # Valida si el valor recibido esta en formato hexadecimal (#739273)
    if not value.startswith('#') or not all(c in '0123456789ABCDEFabcdef' for c in value[1:]): return False
    else: return True  

def validate_username(username):
    # Valida que el username este como lo pide django
    if not re.match(r'^[\w.@+-]+$', username): return False
    else: return True

def validate_email(value):
    # Valida que sea un mail valido
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value): return False
    else: return True

def is_valid_slug(text):
    """
    Verifica si un texto dado es un slug válido.
    Un slug válido debe contener solo caracteres alfanuméricos, guiones y/o guiones bajos,
    y no debe comenzar ni terminar con un guion.
    """
    if not isinstance(text, str):
        return False

    slug_pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(slug_pattern, text)) and not text.startswith('-') and not text.endswith('-')   
