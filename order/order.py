from . import functions
from . import models

class Order:
    """
    Represents an order related to the session. When the order is confirmed,
    it is saved in the database. Until then, the order is managed in this class
    and has its CRUD operations in the user interface.
    This helps the efficiency of the system because the amount of database operations required are fewer than 
     interacting directlty to the db, and it helps the interaction with the session
    """
    def __init__(self, request):
        # If there isn't already an order associated with the session the order is created and saved in the session
        self.request = request
        self.session= request.session
        order= self.session.get('order')
        order_id= self.session.get('order_id')

        if not order:
            self.order= {}
            self.session['order']= self.order
            self.order_id= models.Order.objects.latest('created').order_id + 1
            self.session['order_id']= self.order_id
        else:
            self.order= order
            self.order_id= order_id

    def save_order(self, order):
        # The order is saved in the session
        self.order= order
        self.session['order']= self.order

    def increase_quantity_item(self, order_item_info, quantity):
        # The quantity and the price are increased based on the item_info additional information
        order_item= self.get_menu_item(order_item_info)
        menu_item_info= functions.get_menu_item(order_item['id'])
        if order_item:
            for key, val in self.order['menu_items'].items():
                if val == order_item: item_id= key

            self.order['menu_items'][item_id]['quantity']=  int(self.order['menu_items'][item_id]['quantity']) + quantity
            self.order['menu_items'][item_id]['total_price']=  float(self.order['menu_items'][item_id]['total_price']) + float(menu_item_info.price * quantity)

            self.save_order(self.order)

    def decrease_quantity_item(self, order_item_info, quantity):
        # The quantity and the price are decreased based on the item_info additional information
        order_item= self.get_menu_item(order_item_info)
        menu_item_info= functions.get_menu_item(order_item['id'])
        if order_item:
            for key, val in self.order['menu_items'].items():
                if val == order_item: item_id= key

            self.order['menu_items'][item_id]['quantity']=  int(self.order['menu_items'][item_id]['quantity']) - quantity
            self.order['menu_items'][item_id]['total_price']=  float(self.order['menu_items'][item_id]['total_price']) - float(menu_item_info.price*quantity)

            self.save_order(self.order)

    def add_item(self, item_info, branch):
        # If there isn't already an item associated with the session, the order is fulfilled and saved in the session
        if not self.has_menu_items():
            self.order= {
                'menu_items': {
                    1: item_info,
                },
                'branch_slug': branch,
                'ordered_from': 0,
                'paid': False,
                'delivered': False, 
            } 

            self.save_order(self.order)
        else:
            # If there is already an item with the same characteristics in the order, the quantity and the price are increased
            if self.has_menu_item(item_info):
                self.increase_quantity_item(item_info, int(item_info['quantity']))
            # Else, the item is added to the order
            else:
                item_info_id= int(list(self.order['menu_items'].keys())[-1]) + 1
                self.order['menu_items'][item_info_id]= item_info

            self.save_order(self.order)

    def edit_item_info(self, old_item_info, new_item_info):
        # The item information is changed to the new item info
        for key, value in self.order['menu_items'].items():
            if value== old_item_info:
                self.order['menu_items'][key]= new_item_info
                self.save_order(self.order)

    def del_item(self, item_info):
        # The item information is changed to the new item info
        delete_id= None
        for key, value in self.order['menu_items'].items():
            if value== item_info:
                delete_id= key

        if delete_id:
            del self.order['menu_items'][delete_id]
            self.save_order(self.order)
            return delete_id

    def reset_order(self):
        # The order of the session is reseted
        self.order= {}
        self.session['order']= self.order

    def get_order(self): return self.order
    
    def get_order_id(self): return self.order_id

    def get_branch(self): 
        if self.order['branch_slug']: return self.order['branch_slug']
        else: return ''

    def get_menu_item(self, item_info):
        # Getter of an specific menu item in the order
        if not self.order: return 'no_order'
        if not self.order['menu_items']: return 'no_items'
        for key, value in self.order['menu_items'].items():
            if value['id']== item_info['id'] and value['added']== item_info['added'] and value['removed']== item_info['removed'] and value['observation']== item_info['observation']: return value
            
        else: return 'no_item'

    def is_branch(self, branch):
        if self.order:
            if self.order['branch_slug']== branch.slug: return True
            else: return False
        else: return True

    def has_menu_item(self, item_info):
        for key, value in self.order['menu_items'].items():
            if value['id']== item_info['id'] and value['added']== item_info['added'] and value['removed']== item_info['removed'] and value['observation']== item_info['observation']:
                return True
        return False

    def has_menu_items(self):
        if not self.order: return False
        return bool(self.order['menu_items'])



