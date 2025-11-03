# core/views.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve, Resolver404
from django.utils.http import url_has_allowed_host_and_scheme
# Assuming StoreLocation is in 'stores' app
try:
    from stores.models import StoreLocation
except ImportError:
    StoreLocation = None

def set_location(request):
    next_url = request.GET.get('next', '/') # Get redirect URL
    location_id = request.GET.get('location_id')

    # Basic safety check for redirect URL
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        next_url = '/'

    if location_id and StoreLocation:
        try:
            location = StoreLocation.objects.get(pk=location_id, is_active_online=True)
            # Store essential info in session
            request.session['selected_location_id'] = location.id
            request.session['selected_location_ref'] = location.simphony_loc_ref # Store Simphony ref
            request.session['selected_location_name'] = location.name
            messages.info(request, f"Location set to {location.name}.") # Feedback
        except StoreLocation.DoesNotExist:
            messages.error(request, "Invalid location selected.")
    elif 'location_id' in request.GET and not location_id: # User explicitly chose 'All' or 'Clear'
        request.session.pop('selected_location_id', None)
        request.session.pop('selected_location_ref', None)
        request.session.pop('selected_location_name', None)
        messages.info(request, "Location cleared.")

    return redirect(next_url)