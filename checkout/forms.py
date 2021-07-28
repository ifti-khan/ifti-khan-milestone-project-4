# Improting django forms and order model
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    This order class has a meta class that tell django which
    model the order will be associated with and which fields
    we specify to render.
    """
    class Meta:
        model = Order
        fields = ('full_name', 'email_address', 'phone_number',
                  'address_line1', 'address_line2',
                  'town_or_city', 'postcode', 'county',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        This method overrides the default init method and adds placeholders
        and classes. It also removes auto-generated labels and set the
        autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # Dictionary of placeholders for the order form fields
        placeholders = {
            'full_name': 'Full Name',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postcode',
        }

        # Setting the autofocus to true so the cursor will start
        # on the full name field when the page is loaded
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # A loop that iterates through the form fields and adds a star to
        # the placeholders if that from field is required. It also sets the
        # placeholder attributes from the placeholder dictionary to the
        # form fields, a stripe style class and removing all form field labels
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
