from django.shortcuts import render
from .models import CommunityQuestion


def community(request):
    """
    This view returns the community home page
    """
    # Getting community questions
    questions = CommunityQuestion.objects.all()

    templates = 'community/community.html'
    context = {
        'questions': questions,
    }

    return render(request, templates, context)
