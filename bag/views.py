from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BagItem
from roastery.models import Product

@login_required
def bag_detail(request):
    bag_items = BagItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in bag_items)
    return render(request, 'bag/bag_detail.html', {'bag_items': bag_items, 'total_price': total_price})

@login_required
def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bag_item, created = BagItem.objects.get_or_create(user=request.user, product=product)
    bag_item.quantity += 1
    bag_item.save()
    return redirect('bag:bag_detail')

@login_required
def update_bag_item(request, item_id, quantity):
    bag_item = get_object_or_404(BagItem, id=item_id, user=request.user)
    bag_item.quantity = quantity
    bag_item.save()
    return redirect('bag:bag_detail')

@login_required
def remove_from_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, user=request.user)
    bag_item.delete()
    return redirect('bag:bag_detail')
