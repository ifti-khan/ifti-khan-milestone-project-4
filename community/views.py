from django.shortcuts import render, redirect, reverse, get_object_or_404
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
def view_question(request, question_id):
    """
    Viewing a question
    """

    # Getting question using question id
    question = get_object_or_404(Question, pk=question_id)

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'community/view_question.html'
    context = {
        'question': question,

    }

    return render(request, template, context)


@login_required
def add_question(request):
    """
    Adding a question to the db
    """
    # Checking if the request method is post for the form
    # which then checks to see if the form is valid, and
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


@login_required
def delete_question(request, question_id):
    """
    Delete a current question in the db
    """

    # Getting question using question id
    question = get_object_or_404(Question, pk=question_id)
    # Deleting question
    question.delete()
    # Success message to user using toasts informing them that the question
    # has been deleted and redirecting them back to the community page.
    messages.success(
        request, f'Your question - {question.question_title}\
            has been successfully deleted')

    return redirect(reverse('community'))
