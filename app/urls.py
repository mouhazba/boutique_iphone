from django.urls import path

from .views import *

urlpatterns = [
    path('', login_user, name='index'),

    path('home', home, name='home'),
    path('logout', logout_user, name='logout_user'),
    path('register', register, name='register'),

    path('iphone_add', iphone_add, name='iphone_add'),
    path('iphone/<int:id_iphone>', iphone_update, name='iphone_update'),

    path('client_add', client_add, name='client_add'),
    path('client_list', client_list, name='client_list'),
    path('client_edit/<int:id_client>', client_edit, name='client_update'),

    path('client_moratoire_add', client_moratoire_add, name='moratoire_add'),
    path('client_moratoire_list', client_list_moratoire, name='moratoire_list'),
    path('moratoire_edit/<int:id_client>', client_moratoire_edit, name='moratoire_update'),

    path('versement_add', versement_add, name='versement_add'),
    path('versement_list', versement_list, name='versement_list'),
    path('versement_delete/<int:id_client>', versement_delete, name='versement_delete'),

]