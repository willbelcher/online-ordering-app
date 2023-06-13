from django.shortcuts import render

# Contains store selection and account options
def homepage(request):
    return render(request, '/home.html')
