from django.urls import path
from . import views

# Home app URL
urlpatterns = [
    path('', views.community, name='community'),
    path('<int:question_id>/', views.view_question, name='view_question'),

    # add, edit and delete questions urls
    path('ask/', views.add_question, name='ask'),
    path('edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete/<int:question_id>/', views.delete_question,
         name='delete_question'),

    # Add, edit and delete answers urls
    path('add_answer/<int:question_id>/', views.add_answer, name="add_answer"),
    path('edit_answer/<int:question_id>/<int:answer_id>/',
         views.edit_answer, name="edit_answer"),

]
