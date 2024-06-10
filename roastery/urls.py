from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("products/", views.ProductList.as_view(), name="product_list"),
    path("origin/<str:continent_name>/", views.origin_products, name="origin_products"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]