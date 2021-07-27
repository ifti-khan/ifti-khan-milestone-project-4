from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Question
from .forms import QuestionForm

# This will stop non logged in users from gaining access
# to certain urls
from django.contrib.auth.decorators import login_required


def community(request):
    """
    This view returns the community home page
    """
    # Getting community questions and ordering by most recent
    questions = Question.objects.all().order_by(
        '-date_created', '-time_created')

    # context dictionary with keys and values to be
    # used in the rendered html template
    templates = 'community/community.html'
    context = {
        'questions': questions,
    }

    return render(request, templates, context)


@login_required
def add_question(request):
    """
    Adding a question to the db
    """
    # Checking if request is post for the form and request files for
    # the image file, which then checks to see if the form is valid, and
    # if so then save the form.
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.title = request.POST["question_title"]
            data.message = request.POST["question_message"]
            data.user = request.user
            data.save()
            # Message that will inform the user that the question they have
            # asked has been asked
            messages.success(
                request, f'Your question - {data.title}, has successfully\
                    been asked')
            return redirect(reverse('community'))
        else:
            # Error message informing user that the question failed to ask
            messages.error(request, 'Question failed to ask,\
                Please make sure the form is correctly filled in.')
    else:
        form = QuestionForm()

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'community/ask_question.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
