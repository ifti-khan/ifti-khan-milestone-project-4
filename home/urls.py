from django.urls import path
from . import views

# Home app URL
urlpatterns = [
    path('', views.index, name='home')
]
