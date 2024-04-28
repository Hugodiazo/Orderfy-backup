from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.contrib import messages
from .. import functions
from ..models import CustomUser
from restaurants import models as Rmodels
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

# VIEWS USED TO EDIT THE RESTAURANT DB
@login_required
def edit_user(request, restaurant_slug, username):
    # View used to edit the user
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    user= functions.get_user(username)
    if not user: HttpResponseNotFound(f'Couldn`t find an user with username "{username}"')

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']    
        last_name = request.POST['last_name']
        email = request.POST['email']

        error= False
        if len(username) > 150:
            messages.error(request, 'Username must be at most 150 characters.')
            error= True
        if not functions.validate_username(username):
            messages.error(request, 'Username can be of letters, digits and @/./+/-/_ only.')
            error= True
        if len(first_name) > 150:
            messages.error(request, 'First name must be at most 150 characters.')
            error= True
        if len(last_name) > 150:
            messages.error(request, 'Last name must be at most 150 characters.')
            error= True
        if not functions.validate_email(email):
            messages.error(request, 'The email camp must habe the format of an email address.')
            error= True
        if username != user.username and CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            error= True

        if not error:
            change= False
            if username != user.username:
                user.username = username
                change= True
            if first_name != user.first_name:
                user.first_name = first_name
                change= True
            if last_name != user.last_name:
                user.last_name = last_name
                change= True
            if email != user.email:
                user.email = email
                change= True

            if change:
                user.save()
                messages.success(request, 'The user was saved successfully.')

                action = request.POST['action']
                if action == 'save_and_continue_editing':
                    url = reverse('edit_user', args=[restaurant_slug, username])
                    return redirect(url)
                elif action == 'save_and_add_another':
                    url = reverse('db_register', args=[restaurant_slug])
                    return redirect(url)
                elif action == 'save':
                    url = reverse('db_users', args=[restaurant_slug])
                    return redirect(url)
            else:
                messages.warning(request, 'Nothing was changed.')
    params={
        "restaurant": restaurant,
        "user": user,
    }
    return render(request, 'access_user/edit/edit_user.html', params)

@login_required
def edit_ingredient(request, restaurant_slug, ingredient_slug):
    # View used to edit the ingredient
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    ingredient= functions.get_ingredient(ingredient_slug)
    if not ingredient: return HttpResponseNotFound(f'Couldn`t find an ingredient with slug "{ingredient_slug}"')

    if request.method == 'POST':
        name= request.POST['name']
        slug= request.POST['slug']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = ingredient.image
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
        if slug!= ingredient.slug:
            try:
                Rmodels.Ingredient.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                pass
        if not functions.is_image(image):
            messages.error(request, 'The file must be an image.')
            error= True
        if image.size > 10485760:  # 10 MB
            messages.error(request, 'The file exceeds the maximum size permitted (10 MB).')
            error= True

        if not error: 
            change= False
            if name != ingredient.name:
                ingredient.name = name
                change= True
            if slug != ingredient.slug:
                ingredient.slug = slug
                change= True
            if image != ingredient.image:
                ingredient.image = image
                change= True
            if in_stock != ingredient.in_stock:
                ingredient.in_stock = in_stock
                change= True

            if change:
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
            else:
                messages.warning(request, 'Nothing was changed.')

    params={
        "restaurant": restaurant,
        "ingredient": ingredient,
    }
    return render(request, 'access_user/edit/edit_ingredient.html', params)

@login_required
def edit_item_ingredient(request, restaurant_slug, branch_slug, type_slug, item_id, ingredient_slug):
    # View used to edit the menu item ingredient
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
    ingredient= functions.get_ingredient(ingredient_slug)
    if not ingredient: return HttpResponseNotFound(f'Couldn`t find an ingredient with slug "{ingredient_slug}"')
    item_ingredient= functions.get_item_ingredient(menu_item, ingredient)
    if not item_ingredient: return HttpResponseNotFound(f'Couldn`t find the ingredient "{ingredient}" in the item "{menu_item}"')

    if request.method == 'POST':
        name= request.POST['name']
        slug= request.POST['slug']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = ingredient.image
        if 'in_stock' in request.POST:
            in_stock = True
        else:
            in_stock = False
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
        if slug!= ingredient.slug:
            try:
                Rmodels.Ingredient.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                pass
        if not functions.is_image(image):
            messages.error(request, 'The file must be an image.')
            error= True
        if image.size > 10485760:  # 10 MB
            messages.error(request, 'The file exceeds the maximum size permitted (10 MB).')
            error= True

        if not error:
            change_ingredient= False
            change_item_ingredient= False
            if name != ingredient.name:
                ingredient.name = name
                change_ingredient= True
            if slug != ingredient.slug:
                ingredient.slug = slug
                change_ingredient= True
            if image != ingredient.image:
                ingredient.image = image
                change_ingredient= True
            if in_stock != ingredient.in_stock:
                ingredient.in_stock = in_stock
                change_ingredient= True

            if removable != item_ingredient.removable:
                item_ingredient.removable = removable
                change_item_ingredient= True
            if removable:
                if float(removable_price) != float(item_ingredient.price_remove):
                    item_ingredient.price_remove = removable_price
                    change_item_ingredient= True
            if addable != item_ingredient.addable:
                item_ingredient.addable = addable
                change_item_ingredient= True
            if addable:
                if float(addable_price) != float(item_ingredient.price_add):
                    item_ingredient.price_add = addable_price
                    change_item_ingredient= True
            
            if change_ingredient:
                ingredient.save()
                saved= True
            elif change_item_ingredient:
                item_ingredient.save()
                saved= True
            else:
                messages.warning(request, 'Nothing was changed.')
                saved= False

            if saved:
                messages.success(request, 'The ingredient of this menu item was saved successfully.')

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
        
    params={
        "restaurant": restaurant,
        "branch": branch,
        "type": type_of_category,
        "menu_item": menu_item,
        "ingredient": ingredient,
        "item_ingredient": item_ingredient,
    }
    return render(request, 'access_user/edit/edit_item_ingredient.html', params)

@login_required
def edit_menu_item(request, restaurant_slug, branch_slug, type_slug, item_id):
    # View used to edit menu items
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    categories= Rmodels.Category.objects.filter(type_of_category= type_of_category)
    menu_item= functions.get_menu_item(item_id)
    if not menu_item: return HttpResponseNotFound(f'Couldn`t find a menu item with id {item_id}')

    if request.method == 'POST':
        # Si recibe algo por el formulario, guarda los cambios en la base de datos
        error= False
        try:
            category = Rmodels.Category.objects.get(slug= request.POST['category']) 
        except ObjectDoesNotExist:
            messages.error(request, 'The category chosen is not a valid category.')
            error= True
        name = request.POST['name']
        description = request.POST['description']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = menu_item.image
        price = request.POST['price']
        if 'in_stock' in request.POST:
            in_stock = True
        else:
            in_stock = False

        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(description) > 1000:
            messages.error(request, 'The description must be at most 1000 characters.')
            error= True
        if not functions.is_image(image):
            messages.error(request, 'The file must be an image.')
            error= True
        if image.size > 10485760:  # 10 MB
            messages.error(request, 'The file exceeds the maximum size permitted (10 MB).')
            error= True

        if not error:            
            change= False
            if category != menu_item.category:
                menu_item.category = category
                change= True
            if name != menu_item.name:
                menu_item.name = name
                change= True
            if description != menu_item.description:
                menu_item.description = description
                change= True
            if image != menu_item.image:
                menu_item.image = image
                change= True
            if float(price) != float(menu_item.price):
                menu_item.price = price
                change= True
            if in_stock != menu_item.in_stock:
                menu_item.in_stock = in_stock
                change= True
            if change:
                menu_item.save()
                messages.success(request, 'The menu item was saved successfully.')

                action = request.POST['action']
                if action == 'save_and_continue_editing':
                    url = reverse('edit_menu_item', args=[restaurant_slug, branch_slug, type_slug, menu_item.id])
                    return redirect(url)
                elif action == 'save_and_add_another':
                    url = reverse('add_menu_item', args=[restaurant_slug, branch_slug, type_slug, category.slug])
                    return redirect(url)
                
                elif action == 'save':
                    url = reverse('db_menu', args=[restaurant_slug, branch_slug, type_slug])
                    return redirect(url)
            else:
                messages.warning(request, 'Nothing was changed.')

    params={
        "restaurant": restaurant,
        "branch": branch,
        "type": type_of_category,
        "categories": categories,
        "menu_item": menu_item,
    }
    return render(request, 'access_user/edit/edit_menu_item.html', params)

@login_required
def edit_category(request, restaurant_slug, branch_slug, type_slug, category_slug):
    # View used to edit categories
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    types= Rmodels.TypeOfCategory.objects.filter(branch= branch)
    try:
        category= Rmodels.Category.objects.get(slug= category_slug)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Cannot find category with slug: '" + category_slug + "'")
    
    if request.method == 'POST':
        # Si recibe algo por el formulario, guarda los cambios en la base de datos
        try:
            type_of_category_form = Rmodels.TypeOfCategory.objects.get(slug= request.POST['type']) 
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Cannot find type of category with slug: '" + request.POST['type']+ "'")
        name = request.POST['name']
        slug= request.POST['slug']

        error= False
        if type_of_category_form not in types:
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
        if slug!= category.slug:
            try:
                Rmodels.Category.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                pass

        if not error:            
            change= False
            if type_of_category_form != category.type_of_category:
                category.type_of_category = type_of_category_form
                change= True
            if name != category.name:
                category.name = name
                change= True
            if slug != category.slug:
                category.slug = slug
                change= True
            
            if change:
                category.save()
                messages.success(request, 'The menu item was saved successfully.')

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
            else:
                messages.warning(request, 'Nothing was changed.')

    params= {
        'restaurant': restaurant,
        'branch': branch,
        'type': type_of_category,
        'types': types,
        'category': category,
    }
    return render(request, 'access_user/edit/edit_category.html', params)

@login_required
def edit_type(request, restaurant_slug, branch_slug, type_slug):
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    type_of_category= functions.get_type(type_slug)
    if not type_of_category: return HttpResponseNotFound("Cannot find type of category named '" + type_slug + "'")
    branches= Rmodels.Branch.objects.filter(restaurant= restaurant)

    if request.method == 'POST':
        error= False
        try:
            branch = Rmodels.Branch.objects.get(slug= request.POST['branch']) 
        except ObjectDoesNotExist:
            messages.error(request, 'The branch chosen does not exist.')
            error= True
        name = request.POST['name']
        slug = request.POST['slug']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = "default_type_of_category.avif"

        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        if image!= "default_type_of_category.avif":
            if not functions.is_image(image):
                messages.error(request, 'The file must be an image.')
                error= True
            if image.size > 10485760:  # 10 MB
                messages.error(request, 'The file is bigger than the amount permissed (10 MB).')
                error= True
        if slug != type_of_category.slug:
            try:
                Rmodels.TypeOfCategory.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                pass

        if not error:
            change= False
            if branch != type_of_category.branch:
                type_of_category.branch = branch
                change= True
            if name != type_of_category.name:
                type_of_category.name = name
                change= True
            if slug != type_of_category.slug:
                type_of_category.slug = slug
                change= True
            if image != type_of_category.image:
                type_of_category.image= image
                change= True
            if change:
                type_of_category.save()
                messages.success(request, 'The type of category was saved successfully.')

                action = request.POST['action']
                if action == 'save_and_continue_editing':
                    url = reverse('edit_type', args=[restaurant_slug, branch_slug, type_of_category.slug])
                    return redirect(url)
                elif action == 'save_and_add_another':
                    url = reverse('add_type', args=[restaurant_slug, branch_slug])
                    return redirect(url)
                elif action == 'save':
                    url = reverse('db_types', args=[restaurant_slug, branch_slug])
                    return redirect(url)
            else:
                messages.warning(request, 'Nothing was changed.')

    params={
        "restaurant": restaurant,
        "branch": branch,
        "type": type_of_category,
        "branches": branches,
    }
    return render(request, 'access_user/edit/edit_type.html', params)

@login_required
def edit_branch(request, restaurant_slug, branch_slug):
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")

    if request.method== "POST":
        error= False
        change= False
        name= request.POST['name']
        ubication= request.POST['ubication']
        slug= request.POST['slug']
        try:
            image= request.FILES['image']
        except MultiValueDictKeyError:
            image = branch.image

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
        if image != branch.image:
            if not functions.is_image(image):
                messages.error(request, 'The file is not an image.')
                error= True
            if image.size > 10485760:  # 10 MB
                messages.error(request, 'The file is bigger than the amount permissed (10 MB).')
                error= True

        if slug != branch.slug:
            try:
                Rmodels.Branch.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                pass

        if not error:
            if name != branch.name:
                branch.name = name
                change= True
            if slug != branch.slug:
                branch.slug= slug
                change= True
            if ubication != branch.ubication:
                branch.ubication = ubication
                change= True
            if image != branch.image:
                branch.image= image
                change= True
            if change:
                branch.save()
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
            else:
                messages.warning(request, 'Nothing was changed.')
        
    params={
        "restaurant": restaurant,
        "branch": branch,
    }
    return render(request, 'access_user/edit/edit_branch.html', params)

@login_required
def edit_restaurant(request, restaurant_slug):
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to {restaurant.name}`s DataBase')

    if request.method== 'POST':
        error= False
        change= False
        name = request.POST['name']
        slug = request.POST['slug']
        description = request.POST['description']
        if 'logo' in request.FILES:
            logo = request.FILES['logo']
        else:
            logo = restaurant.logo
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = restaurant.image
        primary_color= request.POST['primary_color']
        secondary_color= request.POST['secondary_color']

        if len(name) > 80:
            messages.error(request, 'The name must be at most 80 characters.')
            error= True
        if len(slug) > 20:
            messages.error(request, 'The slug must be at most 20 characters.')
            error= True
        if not functions.is_valid_slug(slug):
            messages.error(request, 'The text introduced in slug is not a valid slug.')
            error= True
        if len(description) > 1000:
            messages.error(request, 'The description must be at most 1000 characters.')
            error= True
        if logo!= restaurant.logo:
            if not functions.is_image(logo):
                messages.error(request, 'The file of the camp "logo" must be an image.')
                error= True
            if logo.size > 10485760:  # 10 MB
                messages.error(request, 'The file of the camp "logo" exceeds the maximum size permitted (10 MB).')
                error= True
        if image!= restaurant.image:
            if not functions.is_image(image):
                messages.error(request, 'The file of the camp "image" must be an image.')
                error= (True)
            if image.size > 10485760:  # 10 MB
                messages.error(request, 'The file of the camp "image" exceeds the maximum size permitted (10 MB).')
                error= True
        if not functions.validate_color_hex(primary_color):
            messages.error(request, f'The primary color must be in hexadecimal format (#123456)')
            error= True
        if not functions.validate_color_hex(secondary_color):
            messages.error(request, f'The secondary color must be in hexadecimal format (#123456)')
            error= True
        if slug!= restaurant.slug:
            try:
                Rmodels.Restaurant.objects.get(slug= slug)
                messages.error(request, 'The slug has already been used, try with another.')
                error= True
            except ObjectDoesNotExist:
                if not error:
                    restaurant.slug= slug
                    change= True
                
        if not error:
            if name != restaurant.name:
                restaurant.name = name
                change= True
            if description != restaurant.description:
                restaurant.description = description
                change= True
            if logo != restaurant.logo:
                restaurant.logo= logo
                change= True
            if image != restaurant.image:
                restaurant.image= image
                change= True
            if primary_color != restaurant.primary_color:
                restaurant.primary_color= primary_color
                change= True
            if secondary_color != restaurant.secondary_color:
                restaurant.secondary_color= secondary_color
                change= True

            if change:
                restaurant.save()
                messages.success(request, 'The restaurant was saved successfully.')

                action = request.POST['action']
                if action == 'save_and_continue_editing':
                    url = reverse('edit_restaurant', args=[restaurant_slug])
                    return redirect(url)
                elif action == 'save':
                    url = reverse('db_home', args=[restaurant_slug])
                    return redirect(url)
            else:
                messages.warning(request, 'Nothing was changed.')
        
    params={
        "restaurant": restaurant,
    }
    return render(request, 'access_user/edit/edit_restaurant.html', params)



