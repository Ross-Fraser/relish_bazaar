from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .forms import PurchaseEnquiryForm, ProductForm
from django.views import generic
from .models import Product, CONTINENT_CHOICES


def index(request):
    continent_list = [
        {'name': 'African', 'image': get_continent_image(0)},
        {'name': 'Asian', 'image': get_continent_image(1)},
        {'name': 'American', 'image': get_continent_image(2)},
    ]
    return render(request, 'index.html', {'continent_list': continent_list})


def get_continent_image(continent_index):
    try:
        return Product.objects.filter(origin_id__continent=continent_index).first().image
    except AttributeError:
        # Handle the case where no products are found for the continent
        return None


class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = "roastery/index.html"
    paginate_by = 6


def origin_products(request, continent_name=None):
    
    if not continent_name:
        return render(request, 'origin_products.html', {
        })
    
    continent_index = next((index for index, name in CONTINENT_CHOICES if name == continent_name), None)
    if continent_index is None:
        products = []
    else:
        products = Product.objects.filter(origin_id__continent=continent_index)
    
    return render(request, 'origin_products.html', {
        'products': products,
        'continent_name': continent_name
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    success_message = request.GET.get('success_message')

    context = {
        'product': product,
        'continent_name': product.origin_id.get_continent_display(),
        'country_name': product.origin_id.get_country_display(),
        'success_message': success_message
    }

    return render(request, 'product_detail.html', context)


def purchase_form(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        form = PurchaseEnquiryForm(request.POST)
        if form.is_valid():
            # Send enquiry email to the store owner
            send_mail(
                subject=f'I would like to purchase a bag of '
                        f'{form.cleaned_data["product_name"]}',
                message=(
                    f'Name: {form.cleaned_data["name"]}\n'
                    f'Address: {form.cleaned_data["address"]}\n'
                    f'Contact Number: {form.cleaned_data["contact_number"]}\n'
                    f'Email Address: {form.cleaned_data["email_address"]}\n'
                    f'Grind: {form.cleaned_data["grind"]}\n'
                    f'Product Price: {form.cleaned_data["product_price"]}'
                ),
                from_email=form.cleaned_data["email_address"],
                recipient_list=[settings.EMAIL_HOST_USER],
            )

            # Send confirmation email to the user
            send_mail(
                subject='Your purchase enquiry has been received',
                message=(
                    f'Thank you for your enquiry,'
                    f'{form.cleaned_data["name"]}.\n\n'
                    f'Here are the details of your enquiry:\n'
                    f'Product Name: {form.cleaned_data["product_name"]}\n'
                    f'Product Price: {form.cleaned_data["product_price"]}\n'
                    f'Grind: {form.cleaned_data["grind"]}\n'
                    'We will contact you shortly with more information.'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data["email_address"]],
            )

            success_message = "Thank you for your enquiry. We will get back " \
                              "to you soon."
            return HttpResponseRedirect(
                f'{reverse("product_detail", args=[product_id])}?success_message={success_message}'
            )
    else:
        form = PurchaseEnquiryForm(initial={
            'product_name': product.name,
            'product_price': product.price
        })

        context = {
            'form': form,
            'product': product,
            'continent_name': product.origin_id.get_continent_display(),
            'country_name': product.origin_id.get_country_display(),
        }

    return render(request, 'purchase_form.html', context)

@login_required
@permission_required('app.add_product', raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to manage_products with a success message
            return redirect(f'{reverse("manage_products")}?success_message=Product created successfully!')
        else:
            # Allow form errors to show on the template
            return render(request, 'roastery/product_form.html', {'form': form})
    else:
        form = ProductForm()
    
    return render(request, 'roastery/product_form.html', {'form': form})




@login_required
def products_list(request):
    products = Product.objects.all()
    success_message = request.GET.get('success_message', None)
    return render(request, 'roastery/product_list.html', {'products': products, 'success_message': success_message})



@login_required
@permission_required('app.change_product', raise_exception=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(f'{reverse("manage_products")}?success_message=Product updated successfully!')

    else:
        form = ProductForm(instance=product)

    success_message = request.GET.get('success_message')

    return render(request, 'roastery/product_form.html', {'form': form, 'success_message': success_message})

@login_required
@permission_required('app.delete_product', raise_exception=True)
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect(f'{reverse("manage_products")}?success_message=Product deleted successfully!')
    else:
        return JsonResponse({'success': False}, status=400)
    
def custom_permission_denied_view(request):
    return render(request, '403.html', status=403)
