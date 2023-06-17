from . import views 
from django.urls import path
urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('view_data', views.view_data, name='view_data'),
    path('chemical_search', views.chemical_search, name='chemical_search'),
    path('synthesis_search', views.synthesis_search, name='synthesis_search'),
    path('chemical_data', views.chemical_data, name='chemical_data'),



] 