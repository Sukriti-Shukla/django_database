from django.urls import path
from .views import synthesis_input
from .views import search_chemicals
from .views import search_precursors
from .views import synthesischemical_list
from .views import synthesischemical_search

urlpatterns = [
    path('synthesis_input', synthesis_input, name='synthesis_input'),
    path('search-chemicals/', search_chemicals, name='search-chemicals'),
    path('search_precursors/', search_precursors, name='search_precursors'),
    path('synthesischemicals/', synthesischemical_list, name='synthesischemical_list'),
    path('synthesischemical_search/', synthesischemical_search, name='synthesischemical_search'),
]