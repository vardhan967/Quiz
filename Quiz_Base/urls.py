"""
URL configuration for the Quiz_Base project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Route for the Django admin site
    path('admin/', admin.site.urls),
    # Include all URLs from the Quiz_App
    path('', include('Quiz_App.urls')),
]
