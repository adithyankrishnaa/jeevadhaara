"""
URL routing configuration for the donors app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Server-rendered MVT Views
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register_donor'),
    path('donors/', views.donor_list, name='donor_list'),
    
    # Interactive Single Page Application (SPA)
    path('app/', views.single_page_app, name='single_page_app'),
    
    # REST API endpoints for Frontend
    path('api/donors/', views.api_donors_list, name='api_donors_list'),
    path('api/register/', views.api_register_donor, name='api_register_donor'),
]
