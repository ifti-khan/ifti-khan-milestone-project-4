from django.shortcuts import render


def community(request):
    """ This view returns the community home page """

    return render(request, 'community/community.html')
