# core/context_processors.py
# Assuming StoreLocation is in 'stores' app, adjust if different
try:
    from stores.models import StoreLocation
except ImportError:
    StoreLocation = None # Handle case where app/model doesn't exist yet

def location_context(request):
    """
    Adds location context to all templates:
    - all_locations: Queryset of active StoreLocation objects
    - selected_location_id: ID of the currently selected location from session
    - selected_location_name: Name of the currently selected location from session
    """
    all_locations = []
    if StoreLocation:
        all_locations = StoreLocation.objects.filter(is_active_online=True)

    selected_location_id = request.session.get('selected_location_id', None)
    selected_location_name = request.session.get('selected_location_name', None)

    # Optionally try to fetch the name if only ID is in session
    if selected_location_id and not selected_location_name and StoreLocation:
        try:
            location = StoreLocation.objects.get(id=selected_location_id)
            selected_location_name = location.name
            request.session['selected_location_name'] = selected_location_name # Store name too
        except StoreLocation.DoesNotExist:
            # Clear potentially invalid session data
            request.session.pop('selected_location_id', None)
            request.session.pop('selected_location_ref', None)
            selected_location_id = None


    return {
        'all_locations': all_locations,
        'selected_location_id': selected_location_id,
        'selected_location_name': selected_location_name,
    }