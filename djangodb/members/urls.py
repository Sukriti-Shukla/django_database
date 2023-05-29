from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('main_page', views.main_page, name='main_page'), 
    path('logout_user', views.logout_user, name='logout'),  
    path('register_user', views.register_user, name='register_user'),
] 
