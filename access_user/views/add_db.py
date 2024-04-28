from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from restaurants import models as Rmodels
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from .. import functions

# VIEWS USED TO ADD SOMETHING INTO THE RESTAURANT DB
@login_required
def add_ingredient(request, restaurant_slug):
    # View used to add an ingredient
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    if request.method== 'POST':
        name = request.POST['name']
        slug = request.POST['slug']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image= 'default_ingredient.png'
        if 'in_stock' in request.POST:
            in_stock = True
        else:
            in_stock = False

        error= False
        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        try:
            Rmodels.Category.objects.get(slug= slug)
            messages.error(request, 'The slug has already been used, try with another.')
            error= True
        except ObjectDoesNotExist:
            pass
        if image!= 'default_ingredient.png':
            if not functions.is_image(image):
                messages.error(request, 'The file must be an image.')
                error= True
            if image.size > 10485760:  # 10 MB
                messages.error(request, 'The file exceeds the maximum size permitted (10 MB).')
                error= True

        if not error:  
            ingredient= Rmodels.Ingredient(restaurant= restaurant, name= name, slug= slug, image= image, in_stock= in_stock)
            ingredient.save()
            messages.success(request, 'The ingredient was saved successfully.')

            action = request.POST['action']
            if action == 'save_and_continue_editing':
                url = reverse('edit_ingredient', args=[restaurant_slug, ingredient.slug])
                return redirect(url)
            
            elif action == 'save_and_add_another':
                url = reverse('add_ingredient', args=[restaurant_slug])
                return redirect(url)
            
            elif action == 'save':
                url = reverse('db_ingredients', args=[restaurant_slug])
                return redirect(url)

    params={
        "restaurant": restaurant,
    }
    return render(request, 'access_user/add/add_ingredient.html', params)

@login_required
def add_item_ingredient(request, restaurant_slug, branch_slug, type_slug, item_id):
    # View used to add an item ingredient
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    menu_item= functions.get_menu_item(item_id)
    if not menu_item: return HttpResponseNotFound(f'Couldn`t find a menu item with id {item_id}')
    ingredients= Rmodels.Ingredient.objects.filter(restaurant= restaurant)

    if request.method == 'POST':
        error= False
        try:
            ingredient= Rmodels.Ingredient.objects.get(slug= request.POST['ingredient'])
        except ObjectDoesNotExist:
            messages.error(request, 'The ingredient chosen does not exist.')
            error= True
        except MultiValueDictKeyError:
            messages.error(request, 'There are not ingredients added yet, you have to add one first.')
            error= True
        if 'removable' in request.POST:
            removable = True
            removable_price= request.POST['remove_price']
        else:
            removable = False
            removable_price= 0
        if 'addable' in request.POST:
            addable = True
            addable_price= request.POST['add_price']
        else:
            addable = False
            addable_price= 0

        if not error:
            try:
                menu_item_ingredient= Rmodels.MenuItemIngredient(ingredient= ingredient, menu_item= menu_item, removable= removable, price_remove= removable_price, addable= addable, price_add= addable_price)
                menu_item_ingredient.save()
                messages.success(request, 'The menu item ingredient was saved successfully.')

                action = request.POST['action']
                if action == 'save_and_continue_editing':
                    url = reverse('edit_item_ingredient', args=[restaurant_slug, branch_slug, type_slug, item_id, ingredient.slug])
                    return redirect(url)
                elif action == 'save_and_add_another':
                    url = reverse('add_item_ingredient', args=[restaurant_slug, branch_slug, type_slug, item_id])
                    return redirect(url)
                
                elif action == 'save':
                    url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
                    return redirect(url)
            except IntegrityError:
                messages.error(request, 'The menu item has already have this ingredient')

    params={
        'restaurant': restaurant,
        'branch': branch,
        'type': type_of_category,
        'menu_item': menu_item,
        'ingredients': ingredients,
    }
    return render(request, 'access_user/add/add_item_ingredient.html', params)

@login_required
def add_menu_item(request, restaurant_slug, branch_slug, type_slug, category_slug):
    # View used to add a menu item
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    categories= Rmodels.Category.objects.filter(type_of_category= type_of_category)
    try:
        category= Rmodels.Category.objects.get(slug= category_slug)
    except ObjectDoesNotExist:
        if not type_of_category: return HttpResponseNotFound("Cannot find category named '" + category_slug + "'")

    if request.method == 'POST':
        name = request.POST['name']
        if request.POST['description']:
            description = request.POST['description']
        else:
            description= ""
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image= 'default_menu_item.jpg'
        price = request.POST['price']
        if 'in_stock' in request.POST:
            in_stock = True
        else:
            in_stock = False

        error= False
        if category not in categories:
            messages.error(request, 'The category chosen is not a valid category.')
            error= True
        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(description) > 1000:
            messages.error(request, 'The description must be at most 1000 characters.')
            error= True
        if image!= 'default_menu_item.jpg':
            if not functions.is_image(image):
                messages.error(request, 'The file must be an image.')
                error= True
            if image.size > 10485760:  # 10 MB
                messages.error(request, 'The file exceeds the maximum size permitted (10 MB).')
                error= True

        if not error:  
            menu_item= Rmodels.MenuItem(category= category, name= name, description= description, image= image, price= price, in_stock= in_stock)
            menu_item.save()
            messages.success(request, 'The menu item was saved successfully.')

            action = request.POST['action']
            if action == 'save_and_continue_editing':
                url = reverse('edit_menu_item', args=[restaurant_slug, branch_slug, type_slug, menu_item.id])
                return redirect(url)
            elif action == 'save_and_add_another':
                url = reverse('add_menu_item', args=[restaurant_slug, branch_slug, type_slug, category_slug])
                return redirect(url)
            
            elif action == 'save':
                url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
                return redirect(url)

    params={
        'restaurant': restaurant,
        'branch': branch,
        'type': type_of_category,
        'categories': categories,
        'category': category,
    }
    return render(request, 'access_user/add/add_menu_item.html', params)

@login_required
def add_category(request, restaurant_slug, branch_slug, type_slug):
    # View used to add a category
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    types_of_category= Rmodels.TypeOfCategory.objects.filter(branch=branch)

    if request.method == 'POST':
        # Si recibe algo por el formulario, guarda los cambios en la base de datos
        try:
            print(request.POST['type'])
            type_of_category_form = Rmodels.TypeOfCategory.objects.get(slug= request.POST['type']) 
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Cannot find type of category with slug: '" + request.POST['type']+ "'")
        name = request.POST['name']
        slug= request.POST['slug']

        error= False
        if type_of_category_form not in types_of_category:
            messages.error(request, 'The type of category chosen does not exist.')
            error= True
        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        try:
            Rmodels.Category.objects.get(slug= slug)
            messages.error(request, 'The slug has already been used, try with another.')
            error= True
        except ObjectDoesNotExist:
            pass

        if not error:
            category= Rmodels.Category(type_of_category= type_of_category_form, name= name, slug= slug)
            category.save()
            messages.success(request, 'The category was saved successfully.')

            action = request.POST['action']
            if action == 'save_and_continue_editing':
                url = reverse('edit_category', args=[restaurant_slug, branch.slug, type_slug, category.slug])
                return redirect(url)
            
            elif action == 'save_and_add_another':
                url = reverse('add_category', args=[restaurant_slug, branch.slug, type_slug])
                return redirect(url)
            
            elif action == 'save':
                url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
                return redirect(url)

    params={
        'restaurant': restaurant,
        'branch': branch,
        'type': type_of_category,
        'types': types_of_category,
    }
    return render(request, 'access_user/add/add_category.html', params)

@login_required
def add_type(request, restaurant_slug, branch_slug):
    # View used to add a type of category
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")

    if request.method == 'POST':
        # Si recibe algo por el formulario, guarda los cambios en la base de datos
        error= False
        try:
            branch_form= Rmodels.Branch.objects.get(slug= request.POST['branch'])
        except ObjectDoesNotExist:
            messages.error(request, 'The branch chosen does not exist.')
            error= True
        name= request.POST['name']
        slug= request.POST['slug']
        try:
            image= request.FILES['image']
        except MultiValueDictKeyError:
            image = 'default_type_of_category.avif'

        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        if image != 'default_type_of_category.avif':
            if not functions.is_image(image):
                messages.error(request, 'The file is not an image.')
                error= True
        try:
            Rmodels.TypeOfCategory.objects.get(slug= slug)
            messages.error(request, 'The slug has already been used, try with another.')
            error= True
        except ObjectDoesNotExist:
            pass

        if not error:
            type_of_category1= Rmodels.TypeOfCategory(branch= branch_form, name= name, slug= slug, image= image)
            type_of_category1.save()
            messages.success(request, 'The type of category was saved successfully.')

            action = request.POST['action']
            if action == 'save_and_continue_editing':
                url = reverse('edit_type', args=[restaurant_slug, branch_slug, type_of_category1.slug])
                return redirect(url)
            elif action == 'save_and_add_another':
                url = reverse('add_type', args=[restaurant_slug, branch_slug])
                return redirect(url)
            
            elif action == 'save':
                url = reverse('db_types', args=[restaurant_slug, branch_slug])
                return redirect(url)

    params={
        'restaurant': restaurant,
        'branch': branch,
    }
    return render(request, 'access_user/add/add_type.html', params)

@login_required
def add_branch(request, restaurant_slug):
    # View used to add a type of category
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    if request.method== "POST":
        error= False
        name= request.POST['name']
        ubication= request.POST['ubication']
        slug= request.POST['slug']
        try:
            image= request.FILES['image']
        except MultiValueDictKeyError:
            image = 'default_branch.png'

        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(ubication) > 200:
            messages.error(request, 'The ubication must be at most 200 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        if image != 'default_branch.png':
            if not functions.is_image(image):
                messages.error(request, 'The file is not an image.')
                error= True
        try:
            Rmodels.Branch.objects.get(slug= slug)
            messages.error(request, 'The slug has already been used, try with another.')
            error= True
        except ObjectDoesNotExist:
            pass

        if not error:
            branch= Rmodels.Branch(restaurant= restaurant, name= name, ubication= ubication, slug= slug, image= image)
            branch.save()
            restaurant1= Rmodels.Restaurant.objects.get(slug= branch.restaurant.slug)
            restaurant1.q_branches= restaurant1.q_branches + 1
            restaurant1.save()
            messages.success(request, 'The branch was saved successfully.')

            action = request.POST['action']
            if action == 'save_and_continue_editing':
                url = reverse('edit_branch', args=[restaurant_slug, branch.slug])
                return redirect(url)
            
            elif action == 'save_and_add_another':
                url = reverse('add_branch', args=[restaurant_slug])
                return redirect(url)
            
            elif action == 'save':
                url = reverse('db_branches', args=[restaurant_slug])
                return redirect(url)
            
    params={
        'restaurant': restaurant,
    }
    return render(request, 'access_user/add/add_branch.html', params)
   
