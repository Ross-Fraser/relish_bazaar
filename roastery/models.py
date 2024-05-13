from django.db import models

# Create your models here.
GRIND_CHOICES =(
    (0, "Whole Bean"),
    (1, "Coarse"),
    (2, "Medium"),
    (3, "Fine"),
    (4, "Extra Fine")
)


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    main_category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.main_category


class Coffee_Origin(models.Model):
    origin_id = models.AutoField(primary_key=True)
    continent = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.continent


class Coffee_Grind(models.Model):
    grind_id = models.AutoField(primary_key=True)
    grind = models.IntegerField(choices=GRIND_CHOICES, default=0)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.grind


class Coffee_Size(models.Model):
    size_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    coffee_variant = models.ForeignKey(Coffee_Variant, on_delete=models.CASCADE, related_name='products')
    origin_id = models.ForeignKey(Coffee_Origin, on_delete=models.CASCADE, related_name="Coffee_Variants")
    grind_id = models.ForeignKey(Coffee_Grind, on_delete=models.CASCADE, related_name="Coffee_Variants")
    size_id = models.ForeignKey(Coffee_Size, on_delete=models.CASCADE, related_name="Coffee_Variants")
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.manufacturer


class CoffeeVariant(models.Model):
    variant_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Coffee_Products")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Coffee_Products")
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    image = models.ImageField(upload_to='products/')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name