from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

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
    Viewing questions from the db
    """
    # Getting question using question id
    question = get_object_or_404(Question, pk=question_id)

    # Getting answers and filtering by question id and
    # ordering by new answers using date and time
    answers = Answer.objects.filter(
        question=question_id).order_by('-date_created', '-time_created')
    form = AnswerForm(request.POST)

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'community/view_question.html'
    context = {
        'question': question,
        'answers': answers,
        'form': form,

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
            question = form.save(commit=False)
            question.title = request.POST["question_title"]
            question.message = request.POST["question_message"]
            question.user = request.user
            question.save()
            # Message that will inform the user that the question they have
            # asked has been asked
            messages.success(
                request, f'Your question - {question.title}, has successfully\
                    been asked')
            return redirect(reverse('view_question', args=[question.id]))
        else:
            # Error message informing user that the question failed to ask
            messages.error(request, 'Question failed to ask,\
                Please make sure the form is correctly filled in.')
    else:
        form = QuestionForm()

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'community/add_question.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_question(request, question_id):
    """A view to edit questions"""

    # Getting a question using question id
    question = get_object_or_404(Question, pk=question_id)

    # If that checks to see if the logged in user is the
    # user that has asked the question
    if not request.user == question.user:
        messages.warning(
            request, 'Only users that have asked the question, can edit')
        return redirect(reverse('community'))

    # Checking if request user, methods and form are post
    # and if they are then check if the form is valid, if so
    # then the form will save.
    if request.user == question.user:
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                # Message informing the user using toasts,
                # that there question has been updated and redirecting them.
                messages.success(request, 'Your question has been updated')
                return redirect(reverse('view_question', args=[question.id]))
            else:
                # Error message if question fails to update and
                # then redirecting them
                messages.error(
                    request, 'Failed to update question.\
                        Please ensure the form is valid.')
                return redirect(reverse('view_question', args=[question.id]))
        else:
            form = QuestionForm(instance=question)

        # context dictionary with keys and values to be
        # used in the rendered html template
        template = 'community/edit_question.html'
        context = {
            'form': form,
        }
        return render(request, template, context)
    else:
        return redirect(reverse('view_question', args=[question.id]))


@login_required
def delete_question(request, question_id):
    """
    Delete a current question in the db
    """

    # Getting question using question id
    question = get_object_or_404(Question, pk=question_id)

    # If that checks to see if the logged in user is the
    # user that has asked the question
    if not request.user == question.user:
        messages.warning(
            request, 'Only users that have asked the question, can delete')
        return redirect(reverse('community'))

    # Deleting question
    question.delete()
    # Success message to user using toasts informing them that the question
    # has been deleted and redirecting them back to the community page.
    messages.success(
        request, f'Your question - {question.question_title}\
            has been successfully deleted')

    return redirect(reverse('community'))


@login_required
def add_answer(request, question_id):
    """ Adding an answer to a question """
    # Getting question
    question = get_object_or_404(Question, pk=question_id)

    # Checking if request is post and form is post and if it is
    # check if the form is valid and then save the form.
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.message = request.POST["answer_message"]
            data.user = request.user
            data.question = question
            data.save()
            # Message informing the user using toasts,
            # that there answer has been added and redirecting them.
            messages.success(request, 'Thank you for leaving an answer')
            return redirect(reverse('view_question', args=[question.id]))
        else:
            # Error message if answer fails to add
            messages.error(
                request, 'Failed to add your answer.')
    else:

        form = AnswerForm()

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'community/includes/add_answer.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_answer(request, question_id, answer_id):
    """A view to edit an answer"""
    # Getting both questions and answers
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, question=question, pk=answer_id)

    # If that checks to see if the logged in user is the
    # user that has asked the question
    if not request.user == answer.user:
        messages.warning(
            request, 'Only users that have answered the question, can edit')
        return redirect(reverse('community'))

    # Checking if request user and methods are post and form is post
    # and if they are then check if the form is valid and then save the form.
    if request.user == answer.user:
        if request.method == "POST":
            form = AnswerForm(request.POST, instance=answer)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                # Message informing the user using toasts,
                # that there answer has been updated and redirecting them.
                messages.success(request, 'Your answer has been updated')
                return redirect(reverse('view_question', args=[question.id]))
            else:
                # Error message if answer fails to update and redirecting them
                messages.error(
                    request, 'Failed to update answer.\
                        Please ensure the form is valid.')
                return redirect(reverse('view_question', args=[question.id]))
        else:
            form = AnswerForm(instance=answer)

        # context dictionary with keys and values to be
        # used in the rendered html template
        template = 'community/edit_answer.html'
        context = {
            'form': form,
        }
        return render(request, template, context)
    else:
        return redirect(reverse('view_question', args=[question.id]))


@login_required
def delete_answer(request, question_id, answer_id):
    """A view to delete an answer"""
    # Getting both questions and answers
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, question=question, pk=answer_id)

    # If that checks to see if the logged in user is the
    # user that has asked the question
    if not request.user == answer.user:
        messages.warning(
            request, 'Only users that have answered the question, can delete')
        return redirect(reverse('community'))

    # Checking if the user logged in is the user that left the answer
    # and if true then the answer will be deleted.
    if request.user == answer.user:
        answer.delete()
        # Message using toasts to inform user that they
        # have deleted there answer
        messages.success(request, 'Your answer has successfully been deleted')

    return redirect(reverse('view_question', args=[question.id]))
