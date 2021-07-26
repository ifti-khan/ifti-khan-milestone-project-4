from django.shortcuts import render
# This is for the secret keys in the settings
from django.conf import settings

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
