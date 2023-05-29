
from . import views as accounts_views
from django.contrib import admin
from django.urls import include, path  # make sure to import 'include'
from django.contrib.auth import views as auth_views  # import auth views

urlpatterns = [
    path('register', accounts_views.register, name='register'),
    # more paths can be added here
    path('admin', admin.site.urls),
    path('accounts', include('accounts.urls')),  # include the urls from the 'accounts' app
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
]
