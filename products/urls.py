from django.urls import path
from . import views

# All product app URLs
urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>', views.product_details, name='product_details'),
]
