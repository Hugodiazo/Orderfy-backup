from django.urls import path
from .views import access_control
from .views import show_db
from .views import edit_db
from .views import add_db
from .views import delete_db
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Access control paths
    path('<str:restaurant_slug>/logout/', access_control.logout1, name='db_logout'),
    path('<str:restaurant_slug>/register/', login_required(access_control.register), name='db_register'),

    # View sth paths
    path('<str:restaurant_slug>/users/', login_required(show_db.users), name='db_users'),
    path('<str:restaurant_slug>/ingredients/', login_required(show_db.ingredients), name='db_ingredients'), 
    path('<str:restaurant_slug>/', login_required(show_db.home), name='db_home'),
    path('<str:restaurant_slug>/branches', login_required(show_db.branches), name='db_branches'),
    path('<str:restaurant_slug>/<str:branch_slug>/types', login_required(show_db.types), name='db_types'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/menu', login_required(show_db.menu), name='db_menu'),

    # Edit sth paths
    path('<str:restaurant_slug>/<str:username>/edit_user', login_required(edit_db.edit_user), name='edit_user'),
    path('<str:restaurant_slug>/<str:ingredient_slug>/edit_ingredient', login_required(edit_db.edit_ingredient), name='edit_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<int:item_id>/edit_item_ingredient/<str:ingredient_slug>', login_required(edit_db.edit_item_ingredient), name='edit_item_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/edit_menu_item/<int:item_id>', login_required(edit_db.edit_menu_item), name='edit_menu_item'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/edit_category/<str:category_slug>', login_required(edit_db.edit_category), name='edit_category'),
    path('<str:restaurant_slug>/<str:branch_slug>/edit_type/<str:type_slug>', login_required(edit_db.edit_type), name='edit_type'),
    path('<str:restaurant_slug>/edit_branch/<str:branch_slug>/', login_required(edit_db.edit_branch), name='edit_branch'),
    path('<str:restaurant_slug>/edit_restaurant', login_required(edit_db.edit_restaurant), name= 'edit_restaurant'),

    # Add sth paths
    path('<str:restaurant_slug>/add_ingredient', login_required(add_db.add_ingredient), name= 'add_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<int:item_id>', login_required(add_db.add_item_ingredient), name='add_item_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<str:category_slug>/add_menu_item/', login_required(add_db.add_menu_item), name='add_menu_item'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/add_category/', login_required(add_db.add_category), name='add_category'),
    path('<str:restaurant_slug>/<str:branch_slug>/add_type/', login_required(add_db.add_type), name='add_type'),
    path('<str:restaurant_slug>/add_branch/', login_required(add_db.add_branch), name='add_branch'),

    # Delete sth paths
    path('<str:restaurant_slug>/delete_user/<str:username>', login_required(delete_db.delete_user), name='delete_user'),
    path('<str:restaurant_slug>/delete_ingredient/<str:ingredient_slug>', login_required(delete_db.delete_ingredient), name='delete_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<int:item_id>/<str:ingredient_slug>', login_required(delete_db.delete_item_ingredient), name='delete_item_ingredient'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<int:item_id>/delete_menu_item/', login_required(delete_db.delete_menu_item), name='delete_menu_item'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/<str:category_slug>/delete_category/', login_required(delete_db.delete_category), name='delete_category'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_slug>/delete_type/', login_required(delete_db.delete_type), name='delete_type'),
    path('<str:restaurant_slug>/<str:branch_slug>/delete_branch/', login_required(delete_db.delete_branch), name='delete_branch'),
]
