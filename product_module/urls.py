from django.urls import path
from . import views

urlpatterns = [
    path('create_product/', views.CreateProduct.as_view(), name='create_product_page'),
    path('product-detail/<int:product_id>', views.ProductDetail.as_view(), name='product_detail_page'),
]
