from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# --- Remove import for 'home' view ---
# from menu.views import home
# --- Import TemplateView ---
from django.views.generic import TemplateView # Make sure this import is present

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Use TemplateView for the root URL ---
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # --- Application includes (Ensure namespaces match app_name) ---
    path('menu/', include('menu.urls', namespace='menu')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('core/', include('core.urls', namespace='core')),

    # Include users app URLs from root
    path('', include('users.urls', namespace='users')),

]

# Media files handling in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)