from django.urls import path
from . import views

# All the shopping trolley URLs
urlpatterns = [
    path('', views.view_trolley, name='view_trolley'),
    path('add/<item_id>/', views.add_to_trolley, name='add_to_trolley'),
    path('adjust/<item_id>/', views.adjust_trolley, name='adjust_trolley'),
    path('remove/<item_id>/', views.remove_from_trolley,
         name='remove_from_trolley'),
]
