# Importing ClearableFileInput from Django
from django.forms.widgets import ClearableFileInput
# This is not needed but is used to keep custom class, as
# close to the original as possible
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    # Overriding the checkbox button, initial text, input text
    # and template name and setting my own values
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    template_name = (
        'products/custom_widget_templates/custom_clearable_file_input.html')
