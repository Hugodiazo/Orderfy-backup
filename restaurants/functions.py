from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from . import models

# Views.py
def get_restaurant(slug):
    # Devuelve un restoran con slug especifico
    try:
        return models.Restaurant.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return None
    
def get_branch(b_slug, rest):
    # Devuelve una branch con slug y restoran relacionado especifico
    try:
        return models.Branch.objects.get(slug=b_slug, restaurant=rest)
    except ObjectDoesNotExist:
        return None

def get_type(t_slug, branch):
    try:
        type_of_category = models.TypeOfCategory.objects.get(slug=t_slug, branch= branch)
        return type_of_category
    except ObjectDoesNotExist:
        return None

def get_menu_items(categories):
    # Devuelve un diccionario que contiene que la key la categoria y en el value todos los mnue_items relacionados
    menu_items= {}
    for category in categories:
        i= models.MenuItem.objects.filter(category= category)
        menu_items[category.name]= i

    return menu_items

# Models.py
def validate_color_hex(value):
    # Valida si el valor recibido esta en formato hexadecimal (#739273)
    if not value.startswith('#') or not all(c in '0123456789ABCDEFabcdef' for c in value[1:]):
        raise ValidationError("The color must be in hexadecimal format.")
    
def validate_not_zero(value):
    # Valida si el valor recibido es distinto a 0
    if value == 0:
        raise ValidationError("The quantity cannot be zero.")

