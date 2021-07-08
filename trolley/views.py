from django.shortcuts import render

# Create your views here.


def view_trolley(request):
    """
    A view that renders the trolley page
    and its contents
    """

    return render(request, 'trolley/trolley.html')
