"""
URL configuration for education project.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
]
