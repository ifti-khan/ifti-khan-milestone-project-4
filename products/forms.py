from django import forms
from .models import Product, Category, Review
from crispy_forms.helper import FormHelper

# Importing custom image field widget
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    # dunder or __all__ means all fields will be included in the form
    class Meta:
        model = Product
        fields = '__all__'

    # Replacing current image field with custom image widget
    product_image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    # Overriding the init method to make changes to the fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Getting all categories
        categories = Category.objects.all()
        # Creating a tuple for the category friendly names using
        # list comprehension which is a short hand way of creating a for loop
        category_friendly_name = [(
            cat.id, cat.get_friendly_name()) for cat in categories]

        # Updating the categories on the form to use the friendly names
        self.fields['category'].choices = category_friendly_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-0'


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('review_title', 'review_message', 'review_rating',)

    review_message = forms.CharField(widget=forms.Textarea
                                     (attrs={"rows": 3}),)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'review_title': 'Review Title',
            'review_message': 'Type review here',
            'review_rating': 'Product Rating',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[
                field].widget.attrs['class'] = 'rounded-0 review-form'
            self.fields[field].label = False
