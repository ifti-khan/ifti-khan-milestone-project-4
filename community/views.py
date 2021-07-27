from django.shortcuts import render
from .models import CommunityQuestion


def community(request):
    """
    This view returns the community home page
    """
    # Getting community questions and ordering by most recent
    questions = CommunityQuestion.objects.all().order_by(
        '-date_created', '-time_created')

    # context dictionary with keys and values to be
    # used in the rendered html template
    templates = 'community/community.html'
    context = {
        'questions': questions,
    }

    return render(request, templates, context)
