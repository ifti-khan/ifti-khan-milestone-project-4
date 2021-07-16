from django.urls import path
from . import views

# Checkout app URL
urlpatterns = [
    path('', views.checkout, name='checkout')
]
