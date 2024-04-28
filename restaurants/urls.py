
from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurants, name='restaurants'),
    path('<str:restaurant_slug>', views.restaurant, name='restaurant'),
    path('<str:restaurant_slug>/<str:branch_slug>', views.branches, name= 'branches'),
    path('<str:restaurant_slug>/<str:branch_slug>/<str:type_of_category_slug>', views.types, name= 'types'),
]
