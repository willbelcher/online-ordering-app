from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from order.models import Store

import datetime
from zoneinfo import ZoneInfo

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
    return redirect('/store-selection') 

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
                return redirect('/store-selection')   

    return redirect('/')

def user_logout(request):
    logout(request)

    return redirect('/')

@login_required
def store_selection(request):
    user = request.user

    stores = Store.objects.all()
    
    processed_stores = []
    for store in stores:
        is_open = True

        schedule = store.schedule.__dict__
        del schedule['_state']
        del schedule['id']
        schedule = list(schedule.values())

        if store.out_of_schedule_close:
            is_open = False

        else:
            
            timezone = ZoneInfo(store.timezone)
            
            localized_datetime = datetime.datetime.now(tz=timezone)
            current_day = localized_datetime.weekday()
            localized_time = localized_datetime.time()

            today_open = schedule[current_day*2]
            today_close = schedule[current_day*2 + 1]

            if today_open is None or today_close is None:
                is_open = False
            elif localized_time < today_open or localized_time > today_close:
                is_open = False
        
        # Convert BusinessHours model to usable dict
        processed_schedule = {}
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for weekday in weekdays:
            start_time = schedule.pop(0)
            end_time = schedule.pop(0)
            if start_time is None or end_time is None:
                processed_schedule[weekday] = "Closed"
            else:
                processed_schedule[weekday] = f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"

        processed_store = store.__dict__
        del processed_store['_state']
        del processed_store['timezone']

        processed_store['is_open'] = is_open
        processed_store['schedule'] = processed_schedule

        print(processed_store)
        processed_stores.append(
            processed_store
        )

    return render(request, 'order/store_selection.html', {"stores": processed_stores})