# contact/urls.py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # Maps to /contact/
    path('', views.contact_view, name='contact'),
]