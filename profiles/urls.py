from django.urls import path
from . import views

# URL for profiles app
urlpatterns = [
    path('', views.profile, name='profile')
]
