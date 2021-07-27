from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    # Changing the question admin columns
    # using the list display attribute
    list_display = (
        'user',
        'question_title',
        'question_message',
        'date_created',
        'time_created',

    )

    # Sorting the question admin columns
    ordering = ('-date_created', '-time_created')


admin.site.register(Question, QuestionAdmin)
