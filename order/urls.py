from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('create-account/', views.user_create, name='create_account'),
    path('logout/', views.user_logout, name='logout'),
    path('store-selection/', views.store_selection, name='store_selection'),
    path('<int:store_id>/menu/', views.create_order, name='create_order')
]