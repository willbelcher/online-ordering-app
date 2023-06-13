from django.shortcuts import render

# Contains store selection and account options
def index(request):
    return render(request, 'index.html')
