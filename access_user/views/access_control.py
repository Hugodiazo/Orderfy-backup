from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from ..models import CustomUser
from .. import functions
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

# VIEWS USED TO THE AUTHENTICATION TO THE RESTAURANT DB
@login_required
def register(request, restaurant_slug):
    # View used to register a new user who has access to the restaurant database
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    answer= functions.check_user(request, restaurant)
    if answer== "no_access": return HttpResponseForbidden(f'Your user, {request.user.username}, has not access to add new users into {restaurant.name}`s database.')

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']    
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

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
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            error= True
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            error= True

        if not error:
            hashed_password = make_password(password1)
            CustomUser.objects.create_user(username=username, first_name= first_name, last_name=last_name, email=email, password= hashed_password, restaurant= restaurant)
            messages.success(request, 'Account created successfully.')

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
            
    params= {
        'restaurant': restaurant,
    }
    return render(request, 'registration/register.html', params)

def logout1(request, restaurant_slug):
    # View used to logout the user
    restaurant= functions.get_restaurant(restaurant_slug)
    if not restaurant: return HttpResponseNotFound("Cannot find restaurant named '" + restaurant_slug + "'")
    
    try:
        if request.user.is_authenticated:
            logout(request)
            return render(request, "registration/logout.html")
        else:
            return HttpResponseForbidden("You must be logged in to logout.")
    except Exception as e:
        return HttpResponse(f'Error: {e}')

