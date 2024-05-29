from django.shortcuts import render
from django.views import generic
from .models import Product, CONTINENT_CHOICES

def index(request):
    continent_list = [
        {'name': 'African', 'image': 'images/Relish-Coffee-Africa-Selection-300x300.webp'},
        {'name': 'Asian', 'image': 'images/Relish-Coffee-Asia-Selection-300x300.webp'},
        {'name': 'American', 'image': 'images/Relish-Coffee-America-Selection-300x300.webp'},
    ]
    return render(request, 'index.html', {'continent_list': continent_list})

class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = "roastery/index.html"
    paginate_by = 6

def origin_products(request, continent_name):
    continent_index = next((index for index, name in CONTINENT_CHOICES if name == continent_name), None)
    if continent_index is None:
        # Handle the case where the continent name is not found
        return render(request, 'origin_products.html', {'products': [], 'continent_name': continent_name})

    products = Product.objects.filter(origin_id__continent=continent_index)
    return render(request, 'origin_products.html', {'products': products, 'continent_name': continent_name})
