from django.shortcuts import render
from django.views import generic
from .models import Product


# Create your views here.
class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = "roastery/index.html"
    paginate_by = 6