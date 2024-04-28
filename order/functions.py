from django.core.exceptions import ObjectDoesNotExist
from restaurants import models as Rmodels
from . import models as Omodels
from access_user.models import CustomUser

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

def get_menu_item(item_id):
    try:
        menu_item= Rmodels.MenuItem.objects.get(id=item_id)
        return menu_item
    except ObjectDoesNotExist:
        return None

def get_orders(branch):
    """ 
    Devuelve un diccionario que contiene toda la informacion de los menu items agregados a un pedido con el siguiente formato:
    orders_info= {
        order_id: {
            'info': order,  
            'items': {
                menu_item_id: {
                    'info': menu_item,
                    'ingredients_added': {
                        ingredient_slug: ingredient,
                    },
                    'ingredients_removed': {
                        ingredient_slug: ingredient,
                    }
                }
            }
        }
    }
    """
    orders= Omodels.Order.objects.filter(branch= branch)

    orders_info= {}
    if orders.count() > 0:
        for order in orders:
            order_items= Omodels.MenuItemOrder.objects.filter(order= order)
            items_info= {}

            if order_items.count() > 0:
                for order_item in order_items:
                    ingredients_added_dict= {}
                    ingredients_removed_dict= {}
                    ingredients_added= Omodels.IngredientAddedItemOrder.objects.filter(menu_item_order= order_item)
                    ingredients_removed= Omodels.IngredientRemovedItemOrder.objects.filter(menu_item_order= order_item)

                    if ingredients_added.count() > 0:
                        for ingredient_added in ingredients_added:
                            ingredients_added_dict[ingredient_added.menu_item_ingredient.ingredient.slug]= ingredient_added
                    else:
                        ingredients_added_dict= None
                    
                    if ingredients_removed.count() > 0:
                        for ingredient_removed in ingredients_removed:
                            ingredients_removed_dict[ingredient_removed.menu_item_ingredient.ingredient.slug]= ingredient_removed
                    else:
                        ingredients_removed_dict= None
                    
                    items_info[order_item.id]= {
                        "info": order_item,
                        "ingredients_added": ingredients_added_dict,
                        "ingredients_removed": ingredients_removed_dict,
                    }
            else:
                items_info= None

            orders_info[order.id]= {
                'info': order,
                'items': items_info,
            }

    return orders_info

def get_client(client_id):
    try:
        client= Omodels.ClientInfo.objects.get(id= client_id)
        return client
    except ObjectDoesNotExist:
        return None