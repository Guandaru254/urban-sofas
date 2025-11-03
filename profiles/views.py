from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm  # We'll create this form in the next step

@login_required
def profile(request):
    return render(request, 'profiles/profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profiles/update_profile.html', {'form': form})