"""
URL configuration for Jeevadhaara project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('donors.urls')),
]

# Customize Admin Site Headers
admin.site.site_header = "Jeevadhara Blood Donor Administration"
admin.site.site_title = "Jeevadhara Portal"
admin.site.index_title = "Blood Donor Management Portal"
