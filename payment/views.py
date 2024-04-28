from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from order import functions
from order.order import Order 
from order import models
from django.contrib import messages

# Create your views here.

def index(request, branch_slug):
    # View used to ask the user if he want to pay now or pay after eating.
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")

    order_obj= Order(request)
    order_id= order_obj.get_order_id()

    try:
        order_models= models.Order.objects.get(order_id= order_id)
    except: 
        return HttpResponseServerError('An error occurred while connecting with the database.')

    params= {
        'restaurant_slug': branch.restaurant.slug,
        'branch_slug': branch_slug,
        'order': order_models,
    }
    return render(request, 'payment/index.html', params)

def pay_mp(request, branch_slug):
    return render(request, 'payment/pay_mp.html')

def pay_cash(request, branch_slug):
    # View used to change the order.waiting_waiter into true and order.pay_later into false
    branch= functions.get_branch(branch_slug)
    if not branch: return HttpResponseNotFound("Cannot find branch named '" + branch_slug + "'")
    
    order_obj= Order(request)
    order_id= order_obj.get_order_id()

    try:
        order_models= models.Order.objects.get(order_id= order_id)
        order_models.waiting_waiter= True
        order_models.pay_later= False
        order_models.decision_made= True
        order_models.save()

        messages.success(request, 'The waiter was notified, he must be on the way.')
        url = reverse('payment_index', args=[branch_slug])
        return redirect(url)
    except:
        return HttpResponseServerError('An error occurred while notifing the waiter.')


    
