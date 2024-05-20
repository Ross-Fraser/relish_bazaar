from django.contrib import admin
from .models import Category, CoffeeOrigin, CoffeeGrind, CoffeeSize, Product
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):

    list_display = ('name',)
    search_fields = ['name']
    prepopulated_fields = {('name',)}
    summernote_fields = ('description',)
    

# Register your models here.
admin.site.register(Category)
admin.site.register(CoffeeOrigin)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeSize)
