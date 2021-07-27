from django.contrib import admin
from .models import Question, Answer


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


class AnswerAdmin(admin.ModelAdmin):
    # Changing the answer admin columns
    # using the list display attribute
    list_display = (
        'question',
        'user',
        'answer_message',
        'date_created',
        'time_created',

    )

    # Sorting the answer admin columns
    ordering = ('-date_created', '-time_created')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
