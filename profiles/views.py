from django.shortcuts import render, get_object_or_404
# Importing message for toasts to work
from django.contrib import messages

from .models import UserProfile
# Importing the user profile form from forms
from .forms import UserProfileForm

# Importing the order model from the checkout app
from checkout.models import Order

# This will stop non logged in users from gaining access
# to certain urls
from django.contrib.auth.decorators import login_required


@login_required
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
        else:
            # Error message will inform the user, if profile fails to update
            messages.error(request, 'Profile update failed, Please make\
                the form is filled in correctly')
    else:
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


def order_history(request, order_number):
    """
    Getting past order using the order number, then once the
    order number is clicked, the user will be taken to the checkout
    complete page and will be able to see the past order history and
    a toast message informing users that this is a past order.
    """
    order = get_object_or_404(Order, order_number=order_number)

    # Toast message informing user that is a past order
    messages.info(request, (
        f'This is a past order, here is your order number {order_number}. '
        'A confirmation email was sent your on the order date,\
        please check your emails'
    ))

    # setting the template url and returning var to
    # be rendered into the template
    template = 'checkout/checkout_complete.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
