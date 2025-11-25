# core/views.py
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

def set_location(request):
    """Set user's location preference"""
    next_url = request.GET.get('next', '/')
    location_id = request.GET.get('location_id')
    
    # Basic safety check for redirect URL
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        next_url = '/'
    
    try:
        from stores.models import StoreLocation
        
        if location_id:
            try:
                location = StoreLocation.objects.get(pk=location_id, is_active_online=True)
                request.session['selected_location_id'] = location.id
                request.session['selected_location_ref'] = location.simphony_loc_ref
                request.session['selected_location_name'] = location.name
                messages.success(request, f"Location set to {location.name}.")
            except StoreLocation.DoesNotExist:
                messages.error(request, "Invalid location selected.")
        else:
            # Clear location
            request.session.pop('selected_location_id', None)
            request.session.pop('selected_location_ref', None)
            request.session.pop('selected_location_name', None)
            messages.info(request, "Location cleared.")
            
    except Exception as e:
        # Log error but don't crash
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in set_location: {e}")
        messages.error(request, "An error occurred while setting location.")
    
    return redirect(next_url)