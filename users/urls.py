# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views # Django's built-in auth views
from . import views # Your custom views (register, login_user, etc.)

app_name = 'users' # <-- ADD THIS LINE!

urlpatterns = [
    path('register/', views.register, name='register'),
    # Note: Django's default auth URLs also use 'login' and 'logout' names.
    # Using the namespace ('users:login', 'users:logout') prevents conflicts.
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Password Reset URLs using a mix of custom and built-in views
    path(
        'password-reset/',
        views.CustomPasswordResetView.as_view(), # Your custom view (if any)
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]