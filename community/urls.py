from django.urls import path
from . import views

# Home app URL
urlpatterns = [
    path('', views.community, name='community'),
    path('ask/', views.add_question, name='ask'),
]
