from django.shortcuts import render, redirect, reverse
from django.contrib import messages
# This is for the secret keys in the settings
from django.conf import settings
# Django imports to help with sending emails
from django.core.mail import send_mail
from django.template.loader import render_to_string

from profiles.models import UserProfile

# Create your views here.


def index(request):
    """ This view returns the index page """

    return render(request, 'home/index.html')


def about(request):
    """
    This view returns the about us page
    """
    # Google maps api key from setting
    gmaps_api_key = settings.GMAPS_API_KEY

    # Setting template and passing vars to context
    # to be rendered
    template = 'home/about.html'
    context = {
        'gmaps_api_key': gmaps_api_key,
    }

    return render(request, template, context)


def contact(request):
    """
    This view returns the contact us page
    """
    profile = UserProfile.objects.all()
    # Setting template and passing vars to context
    # to be rendered
    template = 'home/contact.html'
    context = {
        'profile': profile
    }

    return render(request, template, context)


def send_contact_email(request):
    """
    Send the site admin an email using the contact form
    """
    # If request method is post, then it will get all of the
    # contact form info and store them in the vars
    if request.method == 'POST':
        contact_user = request.user
        contact_fullname = request.POST['contact-fullname']
        contact_email = request.POST['contact-email']
        contact_subject = request.POST['contact-subject']
        contact_message = request.POST['contact-message']

        # Body var is using the render to string method and
        # passing the values to the contact email body text file
        # to the format i have specified
        body = render_to_string(
            'home/contact_email/contact_email_body.txt',
            {'username': contact_user, 'fullname': contact_fullname,
             'message': contact_message, 'user_email': contact_email,
             'subject': contact_subject})

        # Django send mail method, structure has to be
        # subject, message, from email and to email
        send_mail(
            contact_subject,
            body,
            contact_email,
            [settings.DEFAULT_FROM_EMAIL],
        )
        # Message informing user using toasts that the message
        # has sent and redirecting them to the home page
        messages.success(
            request, 'Your message has been sent to the site admin')
        return redirect(reverse('home'))
    else:
        # Message informing user using toasts that the message
        # failed to send to the admin and redirecting them back
        # to the contact form
        messages.error(
            request, 'Failed to send message to admin')
        return redirect(reverse('contact'))
