"""
URL routing configuration for the donors app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register_donor'),
    path('donors/', views.donor_list, name='donor_list'),
]
