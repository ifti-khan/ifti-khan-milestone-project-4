# Improting django forms and UserProfile model
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    This UserProfile class has a meta class that is telling django
    to render all fields but exclude the user field.
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        This method overrides the default init method and adds placeholders
        and classes. It also removes auto-generated labels and set the
        autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # Dictionary of placeholders for the UserProfile form fields
        placeholders = {
            'default_full_name': 'Full Name',
            'default_email_address': 'Email Address',
            'default_phone_number': 'Phone Number',
            'default_address_line1': 'Address Line 1',
            'default_address_line2': 'Address Line 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Postcode',
        }

        # Setting the autofocus to true so the cursor will start
        # on the full name field when the page is loaded
        self.fields['default_full_name'].widget.attrs['autofocus'] = True

        # A loop that iterates through the form fields and adds a star to
        # the placeholders if that from field is required. It also sets the
        # placeholder attributes from the placeholder dictionary to the
        # form fields, a profile form input class and removing
        # all form field labels
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            self.fields[field].label = False
