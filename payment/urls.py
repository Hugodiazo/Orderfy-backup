
from django.urls import path
from . import views

urlpatterns = [
    path('<str:branch_slug>/', views.index, name='payment_index'),
    path('mercado_pago/<str:branch_slug>/', views.pay_mp, name='pay_mp'),
    path('cash/<str:branch_slug>/', views.pay_cash, name='pay_cash'),
]
