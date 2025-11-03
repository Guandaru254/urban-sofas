# users/views.py (Updated)

from django.shortcuts import render, redirect, reverse # Added reverse
from django.contrib.auth import login, logout, authenticate # Standard auth functions
from django.contrib import messages # For user feedback messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm # Standard forms
from django.contrib.auth.views import PasswordResetView # Standard class-based view
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required # If needed for other views

# --- Import your custom form ---
from .forms import CustomUserCreationForm

# -----------------------------
# Registration View
# -----------------------------
def register(request):
    """ Handles new user registration using the custom form. """
    if request.user.is_authenticated:
        # Redirect logged-in users away from registration page
        return redirect('menu:menu_list')

    if request.method == 'POST':
        # Use the CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves User and creates Profile via form's save method
            login(request, user) # Log the user in immediately after registration
            messages.success(request, f"Welcome, {user.username}! Registration successful and you are now logged in.")
            # Use namespaced redirect to the menu page
            return redirect('menu:menu_list')
        else:
            # Form is invalid, add error message (form should display field errors in template)
            messages.error(request, "Please correct the registration errors below.")
    else: # GET request
        # Use the CustomUserCreationForm
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# -----------------------------
# Login View
# -----------------------------
def login_user(request):
    """ Handles user login using Django's AuthenticationForm. """
    # Redirect logged-in users away from login page
    if request.user.is_authenticated:
        return redirect('menu:menu_list') # Or user profile, or home

    # --- Determine the 'next' URL safely ---
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    # TODO: Add validation here later to ensure 'next_url' is safe/local if needed
    # from django.utils.http import url_has_allowed_host_and_scheme
    # if next_url and not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
    #     next_url = '' # Reset if potentially unsafe redirect

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Use standard login form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"Welcome back, {user.username}!")
            # Redirect to 'next' page if it exists, otherwise default to menu
            if next_url:
                 return redirect(next_url)
            return redirect('menu:menu_list') # Default redirect
        else:
            # Form is invalid (wrong credentials)
            messages.error(request, "Invalid username or password. Please try again.")
    else: # GET request
        form = AuthenticationForm()

    # --- Pass next_url to the template context ---
    context = {
        'form': form,
        'next': next_url # Pass the determined next_url
    }
    return render(request, 'users/login.html', context)

# -----------------------------
# Logout View
# -----------------------------
def logout_user(request):
    """ Logs the current user out. Requires POST request. """
    # Ensure only POST requests trigger logout for security
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been successfully logged out.")
         # Use namespaced redirect to the login page
        return redirect('users:login')
    else:
        # Redirect GET requests for logout URL (e.g., user typed it)
        # Prevent accidental logout via simple link click
        messages.warning(request, "Logout must be done via the logout button.")
        return redirect(request.META.get('HTTP_REFERER', reverse('menu:menu_list'))) # Redirect back or to default


# -----------------------------
# Custom Password Reset View
# -----------------------------
# Uses Django's built-in logic but specifies custom templates/success URL
class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html' # Your template for the email form
    email_template_name = 'users/password_reset_email.html' # Template for the email body
    subject_template_name = 'users/password_reset_subject.txt' # Template for email subject
    # Use namespaced reverse_lazy for the success URL
    success_url = reverse_lazy('users:password_reset_done')
    form_class = PasswordResetForm # Use standard Django form

    # Optional: Add extra context to the email form page if needed
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['site_name'] = "Samaki Samaki" # Example
    #     return context

# Remember that the other password reset views (Done, Confirm, Complete) are
# handled by Django's built-in views specified in users/urls.py,
# using the custom template paths you provided there.
# You need to create those templates:
# - users/password_reset_done.html
# - users/password_reset_confirm.html
# - users/password_reset_complete.html
# - users/password_reset_email.html (email body)
# - users/password_reset_subject.txt (email subject line)