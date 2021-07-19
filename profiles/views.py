from django.shortcuts import render, get_object_or_404
# Importing message for toasts to work
from django.contrib import messages

from .models import UserProfile
# Importing the user profile form from forms
from .forms import UserProfileForm


def profile(request):
    """
    Display the user's profile with user profile form.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    # Checks if method is post it will create a new instance of the
    # user profile form using the profile gotten. Also if the form is
    # valid then save the form and a toast message will display to the
    # user letting them know the profile has been updated.
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    # This populates the profile form with the currents user profile
    # info. Also getting all the order history associated with the user
    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    # setting the template url and returning var to
    # be rendered into the template
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)
