from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    # Meta class is excluding specific fields but including the rest
    class Meta:
        model = Question
        exclude = ('user', 'date_created', 'time_created')

        # Setting the row attribute for the question message
        question_message = forms.CharField(widget=forms.Textarea
                                           (attrs={"rows": 3}),)

    def __init__(self, *args, **kwargs):
        """
        Adding placeholders and classes for question
        form fields, and remove auto-generated crispy form labels
        """
        super().__init__(*args, **kwargs)

        # Setting custom text placeholders
        placeholders = {
            'question_title': 'Question Title',
            'question_message': 'Type your question here',
        }

        # Attaching placeholders, setting class names and removing form labels
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[
                field].widget.attrs['class'] = 'rounded-0 question-form-fields'
            self.fields[field].label = False


class AnswerForm(forms.ModelForm):
    # Meta class is excluding specific fields but including the rest
    class Meta:
        model = Answer
        exclude = ('user', 'question', 'date_created', 'time_created')

        # Setting the row attribute for the answer message
        answer_message = forms.CharField(widget=forms.Textarea
                                         (attrs={"rows": 3}),)

    def __init__(self, *args, **kwargs):
        """
        Adding placeholders and classes for answer
        form field, and remove auto-generated crispy form labels
        """
        super().__init__(*args, **kwargs)

        # Setting custom text placeholders
        placeholders = {
            'answer_message': 'Type your answer here',
        }

        # Attaching placeholders, setting class names and removing form labels
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[
                field].widget.attrs['class'] = 'rounded-0 answer-form-fields'
            self.fields[field].label = False
