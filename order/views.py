from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Contains store selection and account options
def index(request):
    login_error = account_create_error = None
    if 'login_error' in request.session:
        login_error = request.session['login_error']
        del request.session['login_error']
    if 'account_create_error' in request.session:
        account_create_error = request.session['account_create_error']
        del request.session['account_create_error']

    context = {
        'login_error': login_error,
        'account_create_error': account_create_error,
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

    return redirect('/')

def user_create(request):

    return redirect('/', )
