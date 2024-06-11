from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .forms import EnquiryForm
from django.views import generic
from .models import Product, CONTINENT_CHOICES


def index(request):
    continent_list = [
        {'name': 'African', 'image': 'images/coffee/Relish-Coffee-Africa-Selection-300x300.webp'},
        {'name': 'Asian', 'image': 'images/coffee/Relish-Coffee-Asia-Selection-300x300.webp'},
        {'name': 'American', 'image': 'images/coffee/Relish-Coffee-America-Selection-300x300.webp'},
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

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def enquiry_form(request, product_id):
    product = Product.objects.get(product_id=product_id)
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            # Process form data
            send_mail(
                f'Enquiry for {form.cleaned_data["product_name"]}',
                f'Name: {form.cleaned_data["name"]}\n'
                f'Address: {form.cleaned_data["address"]}\n'
                f'Contact Number: {form.cleaned_data["contact_number"]}\n'
                f'Email Address: {form.cleaned_data["email_address"]}\n'
                f'Grind: {form.cleaned_data["grind"]}\n'
                f'Product Price: {form.cleaned_data["product_price"]}',
                'from@example.com',
                ['to@example.com'],
            )
            return redirect('success_page')
    else:
        form = EnquiryForm(initial={'product_name': product.name, 'product_price': product.price})
    
    return render(request, 'enquiry_form.html', {'form': form, 'product': product})

def success_page(request):
    return render(request, 'success_page.html')
