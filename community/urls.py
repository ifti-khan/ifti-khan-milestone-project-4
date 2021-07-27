from django.urls import path
from . import views

# Home app URL
urlpatterns = [
    path('', views.community, name='community'),
    path('ask/', views.add_question, name='ask'),
    path('delete/<int:question_id>/', views.delete_question,
         name='delete_question'),
]
