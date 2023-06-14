from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
    return redirect('/')

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

    return redirect('/')
