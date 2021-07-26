from django.urls import path
from . import views

# Home app URL
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('send/', views.send_contact_email, name='send'),
]
