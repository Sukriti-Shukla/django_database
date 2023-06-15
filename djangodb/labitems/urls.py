from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('input', views.input, name='input'),
    path('input_template', views.input_template, name='input_template'),
    path('index', views.index, name='index'),
    path('update_event/<event_id>', views.update_event, name='update_event'),
    path('delete_event/<event_id>', views.delete_event, name='delete_event'),
    path('upload', views.upload_file, name='upload_file'),
    path('fetch_subtype_fields/', views.fetch_subtype_fields, name='fetch_subtype_fields'),
]