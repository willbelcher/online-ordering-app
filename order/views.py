from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from order.models import Store, Order, OrderMethod, OrderMethods, OrderStatuses, MenuItemCategories
from order.custom_utils import StoreWrapper

# Contains store selection and account options
def index(request):
    login_error = account_create_errors = None
    if 'login_error' in request.session:
        login_error = request.session['login_error']
        del request.session['login_error']
    if 'account_create_errors' in request.session:
        if len(request.session['account_create_errors']) != 0:
            account_create_errors = request.session['account_create_errors']
            request.session['account_create_errors'] = []

    context = {
        'login_error': login_error,
        'account_create_errors': account_create_errors,
    }
    return render(request, 'index.html', context)

def user_login(request):
    logout(request)
    username = password = None

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                request.session['login_error'] = "User account may have been deleted, please contact support"
                return redirect('/')
        else:
            request.session['login_error'] = "Incorrect username/password"
            return redirect('/')

    # print("logged in as: {}".format(request.user))
    return redirect("order:store_selection") 

def user_create(request):
    logout(request)
    username = email = password = None

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        username_taken = email_taken = False
        request.session['account_create_errors'] = []
        if User.objects.filter(username=username).exists():
            username_taken = True
            request.session['account_create_errors'].append('This username is already in use')
            
        if User.objects.filter(email=email.lower()).exists():
            email_taken = True
            request.session['account_create_errors'].append('This email is already in use')
            
        if username_taken or email_taken:
            return redirect('/')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        # print("created new user: {}".format(user.get_username()))

        if user is not None:
            if user.is_active:
                login(request, user) 
                # print("logged in as: {}".format(request.user))
                return redirect("order:store_selection")   

    return redirect("order:index")

def user_logout(request):
    logout(request)

    return redirect("order:index")

@login_required
def store_selection(request):
    user = request.user

    stores = Store.objects.all()
    
    processed_stores = []
    for store in stores:
        store_wrapper = StoreWrapper(store)

        processed_store = store_wrapper.store_to_dict()
        processed_store['is_open'] = store_wrapper.check_is_open()
        processed_store['schedule'] = store_wrapper.schedule_to_dict()

        processed_stores.append(processed_store)

    return render(request, 'order/store_selection.html', {"stores": processed_stores})


@login_required
def create_order(request):
    if request.method != "POST": return redirect("order:store_selection")

    store_id = int(request.POST['store_id']) # check security on this
    user = request.user
    
    current_orders = Order.objects.filter(user=user, status=OrderStatuses.IN_PROGRESS)
    current_orders.delete() # TODO: Change for continue order option, render create_order.html
    
    store = Store.objects.get(id=store_id)
    order_method = store.order_methods.get(method=OrderMethods.PICKUP) #temp TODO: user select order method (in create order and store select)
    
    Order.objects.create(user=user, store=store, order_method=order_method)

    return redirect("order:edit_order")

@login_required
def edit_order(request):
    user = request.user

    orders = Order.objects.defer("store", "date_created").filter(user=user, status=OrderStatuses.IN_PROGRESS)
    if orders.count() != 1: return redirect("order:store_selection")

    order = orders.first()

    menu_items = order.store.available_items

    items_by_category = {category:[] for category in MenuItemCategories.values}
    for menu_item in menu_items.all():
        items_by_category[menu_item.category].append(menu_item)

    context = {
        "items_by_category": items_by_category
    }

    return render(request, "order/edit_order.html", context)







