from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models
from . import functions
from order.order import Order

# Create your views here.

def restaurants(request):
    restaurants= models.Restaurant.objects.all()

    if not restaurants:
        return HttpResponse('OrderFy`s database is empty at the moment.')

    params= {
        "restaurants": restaurants,
    }
    return render(request, 'restaurants/restaurants.html', params)

def restaurant(request, restaurant_slug):
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponse(f"Couldn't find a restaurant with slug '{restaurant_slug}'")
    branches= models.Branch.objects.filter(restaurant= restaurant)
    if not branches:
        return HttpResponse(f'The restaurant {restaurant.name} has no branches.')

    params= {
        "restaurant": restaurant,
        "branches": branches,
        "menu_items": {},
        "types_of_category": {},
    }

    if branches.count() == 1:
        types_of_category= models.TypeOfCategory.objects.filter(branch= branches[0])

        if types_of_category:
            if types_of_category.count()== 1:
                categories= models.Category.objects.filter(type_of_category= types_of_category[0])
                params["menu_items"]= functions.get_menu_items(categories)
            else:
                params["types_of_category"]= types_of_category
        else:
            return HttpResponse(f'The {restaurant.name}`s branch ({branches.first().name}) does not have any type of category')

    return render(request, 'restaurants/restaurant/restaurant.html', params)

def branches(request, restaurant_slug, branch_slug):
    restaurant = functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponse(f"Couldn't find a restaurant with slug '{restaurant_slug}'")
    branch = functions.get_branch(branch_slug, restaurant)
    if not branch: return HttpResponse(f"Couldn't find a branch with slug '{branch_slug}' in restaurant '{restaurant.name}'")
    types_of_category= models.TypeOfCategory.objects.filter(branch= branch)
    order= Order(request)

    params= {
        "restaurant": restaurant,
        "branch": branch,
        "types_of_category": types_of_category,
    }

    if types_of_category.count() == 1:
        categories= models.Category.objects.filter(type_of_category= types_of_category[0])
        params['menu_items']= functions.get_menu_items(categories)
    if order.is_branch(branch): params['order'] = order.get_order()
    else: params['order'] = {}
    return render(request, 'restaurants/restaurant/branches/branches.html', params)

def types(request, restaurant_slug, branch_slug, type_of_category_slug):
    restaurant = functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponse(f"Couldn't find a restaurant with slug '{restaurant_slug}'")
    branch = functions.get_branch(branch_slug, restaurant)
    if not branch: return HttpResponse(f"Couldn't find a branch with slug '{branch_slug}' in restaurant '{restaurant.name}'")
    type_of_category= functions.get_type(type_of_category_slug, branch)
    if not type_of_category: return HttpResponse(f"Couldn't find a type of category with slug '{type_of_category_slug}'")
    order= Order(request)
    
    categories= models.Category.objects.filter(type_of_category= type_of_category)
    menu_items= functions.get_menu_items(categories)

    params= {
        "restaurant": restaurant,
        "branch": branch,
        "type": type_of_category,
        "menu_items": menu_items,
    }
    if order.is_branch(branch): params['order'] = order.get_order()
    else: params['order'] = {}
    return render(request, 'restaurants/restaurant/branches/types.html', params)

