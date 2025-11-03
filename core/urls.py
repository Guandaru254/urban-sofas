# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('set-location/', views.set_location, name='set_location'),
]