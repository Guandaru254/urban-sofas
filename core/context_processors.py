# core/context_processors.py

def location_context(request):
    """
    Adds location context to all templates.
    Wrapped in try-except to prevent 500 errors if database/model issues occur.
    """
    context = {
        'all_locations': [],
        'selected_location_id': None,
        'selected_location_name': None,
    }
    
    try:
        from stores.models import StoreLocation
        
        # Get all active locations
        context['all_locations'] = StoreLocation.objects.filter(is_active_online=True)
        
        # Get selected location from session
        selected_location_id = request.session.get('selected_location_id', None)
        selected_location_name = request.session.get('selected_location_name', None)
        
        context['selected_location_id'] = selected_location_id
        context['selected_location_name'] = selected_location_name
        
        # If ID exists but no name, try to fetch it
        if selected_location_id and not selected_location_name:
            try:
                location = StoreLocation.objects.get(id=selected_location_id)
                context['selected_location_name'] = location.name
                request.session['selected_location_name'] = location.name
            except StoreLocation.DoesNotExist:
                # Clear invalid session data
                request.session.pop('selected_location_id', None)
                request.session.pop('selected_location_ref', None)
                context['selected_location_id'] = None
                
    except Exception as e:
        # Log the error but don't crash the site
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in location_context: {e}")
        # Return empty context - site still works, just no locations
        pass
    
    return context