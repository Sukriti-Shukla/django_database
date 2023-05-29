from . import views 
from django.urls import path
urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
] 