# gallery/views.py

from django.shortcuts import render
from django.templatetags.static import static

def gallery_view(request):
    gallery_images = []
    image_folder = 'assets/images/'
    for i in range(1, 31): # Loop 1 to 30
        image_name = f"{i}.jpg"
        try:
            image_url = static(f"{image_folder}{image_name}")
            gallery_images.append({
                'url': image_url,
                'alt': f"Samaki Samaki Gallery Image {i}"
            })
        except Exception:
            print(f"Warning: Could not find static file for {image_folder}{image_name}")
            pass

    context = {
        'gallery_images': gallery_images
    }
    # --- CHANGE THIS LINE ---
    # OLD: return render(request, 'gallery/gallery.html', context)
    # NEW: Render the template directly from app's templates dir
    return render(request, 'gallery.html', context) # <-- Use this path