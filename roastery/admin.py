from django.contrib import admin
from .models import Category, Coffee_Origin, Coffee_Grind, Coffee_Size, Coffee_Variant, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Coffee_Origin)
admin.site.register(Coffee_Grind)
admin.site.register(Coffee_Size)
admin.site.register(Coffee_Variant)
admin.site.register(Product)
