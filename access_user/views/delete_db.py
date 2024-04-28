from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .. import functions
from django.contrib import messages

# VIEWS USED TO DELETE SOMETHING FROM THE RESTAURANT DB
@login_required
def delete_user(request, restaurant_slug, username):
    # View used to delete the user
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    user= functions.get_user(username)
    if not user: HttpResponseNotFound(f'Couldn`t find an user with username "{username}"')
    user.delete()
    messages.success(request, f'The user "{username}" has been deleted.')

    url = reverse('db_users', args=[restaurant_slug])
    return redirect(url)

@login_required
def delete_ingredient(request, restaurant_slug, ingredient_slug):
    # View used to delete the ingredient
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    ingredient= functions.get_ingredient(ingredient_slug)
    if not ingredient: return HttpResponseNotFound(f'Couldn`t find an ingredient with slug "{ingredient_slug}"')
    ingredient.delete()
    messages.success(request, f'The ingredient "{ingredient.name}" has been deleted.')

    url = reverse('db_ingredients', args=[restaurant_slug])
    return redirect(url)

@login_required
def delete_item_ingredient(request, restaurant_slug, branch_slug, type_slug, item_id, ingredient_slug):
    # View used to delete the menu item ingredient
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    menu_item= functions.get_menu_item(item_id)
    if not menu_item: return HttpResponseNotFound(f'Couldn`t find a menu item with id {item_id}')
    ingredient= functions.get_ingredient(ingredient_slug)
    if not ingredient: return HttpResponseNotFound(f'Couldn`t find an ingredient with slug "{ingredient_slug}"')

    item_ingredient= functions.get_item_ingredient(menu_item, ingredient)
    if not item_ingredient: return HttpResponseNotFound(f'Couldn`t find the ingredient "{ingredient}" in the item "{menu_item}"')
    item_ingredient.delete()
    messages.success(request, f'The menu item ingredient "{ingredient.name}" has been deleted.')

    url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
    return redirect(url)

@login_required
def delete_menu_item(request, restaurant_slug, branch_slug, type_slug, item_id):
    # View used to delete menu items
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    menu_item= functions.get_menu_item(item_id)
    if not menu_item: return HttpResponseNotFound(f'Couldn`t find a menu item with id {item_id}')
    menu_item.delete()
    messages.success(request, f'The menu item "{menu_item.name}" has been deleted.')

    url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
    return redirect(url)

@login_required
def delete_category(request, restaurant_slug, branch_slug, type_slug, category_slug): 
    # View used to delete categories
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    category= functions.get_category(category_slug)
    if not category: return HttpResponseNotFound(f'Couldn`t find a category with slug: {category_slug}')
    category.delete()
    messages.success(request, f'The category "{category.name}" has been deleted.')

    url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
    return redirect(url)

@login_required
def delete_type(request, restaurant_slug, branch_slug, type_slug):
    # View used to delete type of category
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    type_of_category.delete()
    messages.success(request, f'The type of category "{type_of_category.name}" has been deleted.')

    url = reverse('db_types', args=[restaurant_slug, branch_slug])
    return redirect(url)

@login_required
def delete_branch(request, restaurant_slug, branch_slug):
    # View used to delete branch of category
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    branch.delete()
    restaurant.q_branches= restaurant.q_branches - 1
    restaurant.save()
    messages.success(request, f'The branch "{branch.name}" has been deleted.')

    url = reverse('db_branches', args=[restaurant_slug])
    return redirect(url)
