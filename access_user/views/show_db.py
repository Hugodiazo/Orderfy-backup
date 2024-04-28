from django.contrib.auth.decorators import login_required
from .. import functions
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from restaurants import models as Rmodels
from .. import models as Amodels
from django.shortcuts import render

# VIEWS USED TO SHOW THE RESTAURANT DB
@login_required
def users(request, restaurant_slug):
    # View used to show info of the users with acces to this db
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    users= Amodels.CustomUser.objects.filter(restaurant=restaurant)

    params= {
        "restaurant": restaurant,
        "users": users,
    }
    return render(request, 'access_user/info/users.html', params)

@login_required
def ingredients(request, restaurant_slug):
    # View used to show info of the ingredients
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    ingredients= Rmodels.Ingredient.objects.filter(restaurant=restaurant)

    params= {
        "restaurant": restaurant,
        "ingredients": ingredients,
    }
    return render(request, 'access_user/info/ingredients.html', params)

@login_required
def home(request, restaurant_slug):
    # View used to show info of the restaurant and link to change something of it
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    params= {
        "restaurant": restaurant,
        "user": request.user,
    }
    return render(request, 'access_user/db_home.html', params)

@login_required
def branches(request, restaurant_slug):
    # View used to show all the restaurant branches and edit something of them
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branches= Rmodels.Branch.objects.filter(restaurant= restaurant)

    params={
        "restaurant": restaurant,
        "branches": branches,
    }
    return render(request, 'access_user/info/branches.html', params)

@login_required
def types(request, restaurant_slug, branch_slug):
    # View used to show all the branch types of categories and edit something of them
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    types= Rmodels.TypeOfCategory.objects.filter(branch=branch)

    params= {
        'restaurant': restaurant,
        'branch': branch,
        'types': types,
    }
    return render(request, 'access_user/info/types.html', params)

@login_required
def menu(request, restaurant_slug, branch_slug, type_slug):
    # View used to show all the categories and menu items of the type of categories and link to edit something of them
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    menu_items= functions.get_menu_items(type_of_category)

    params={
        "restaurant": restaurant,
        "branch": branch,
        "type": type_of_category,
        "menu_items": menu_items,
    }
    return render(request, 'access_user/info/menu.html', params)

