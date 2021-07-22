from django.urls import path
from . import views

# All product app URLs
urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
]
