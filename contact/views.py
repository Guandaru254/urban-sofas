# contact/views.py (Verified for template path)

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm # Assumes ContactForm is in contact/forms.py

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message']

            full_subject = f"Website Contact Form: {subject}"
            full_message = f"Message from: {name} ({from_email})\n\n{message_body}\n"

            try:
                send_mail(
                    full_subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL, # Sender (from settings)
                    [settings.CONTACT_EMAIL],    # Recipient (from settings)
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully! We'll get back to you soon.", extra_tags='contact_form')
                return redirect('contact:contact') # Redirect back to contact page
            except BadHeaderError:
                 messages.error(request, "Invalid header found in message.", extra_tags='contact_form')
                 return HttpResponse('Invalid header found.')
            except Exception as e:
                print(f"Error sending contact email: {e}") # Log error
                messages.error(request, "Sorry, there was an error sending your message. Please try again later.", extra_tags='contact_form')
                # Re-render the form below if sending fails

        else: # Form is invalid
             messages.error(request, "Please correct the errors below.", extra_tags='contact_form')
             # Fall through to render the template with the invalid form below

    else: # GET request
        form = ContactForm()

    context = {'form': form}
    # --- THIS LINE MUST MATCH YOUR FILE LOCATION ---
    # It renders 'contact.html' found inside the 'contact/templates/' directory
    return render(request, 'contact.html', context) # <-- VERIFIED LINE