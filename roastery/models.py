from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.
GRIND_CHOICES = (
    (0, "Whole Bean"),
    (1, "Coarse"),
    (2, "Medium"),
    (3, "Fine"),
    (4, "Extra Fine")
)


CONTINENT_CHOICES = (
    (0, "African"),
    (1, "Asian"),
    (2, "American"),
)


COUNTRY_CHOICES = (
    (0, "Ethiopia"),
    (1, "Kenya"),
    (2, "Uganda"),
    (3, "India"),
    (4, "Vietnam"),
    (5, "Brazil"),
    (6, "Colombia"),
    (7, "Guatemala"),
    (8, "Peru"),
)


REGION_CHOICES = (
    (0, "Sidamo"),
    (1, "Blue Mountain"),
    (2, "Agua Santa"),
    (3, "Excelso Popayan"),
    (4, "Huehuetenango"),
    (5, "Copaceyba"),
    (6, "Malabar"),
    (7, "-")
)


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    main_category = models.CharField(max_length=100)

    def __str__(self):
        return self.main_category


class CoffeeOrigin(models.Model):
    origin_id = models.AutoField(primary_key=True)
    continent = models.IntegerField(choices=CONTINENT_CHOICES)
    country = models.IntegerField(choices=COUNTRY_CHOICES)
    region = models.IntegerField(choices=REGION_CHOICES)

    def get_continent_display(self):
        return dict(CONTINENT_CHOICES).get(self.continent)

    def get_country_display(self):
        return dict(COUNTRY_CHOICES).get(self.country)

    def get_region_display(self):
        return dict(REGION_CHOICES).get(self.region)

    def __str__(self):
        return f"{self.get_continent_display()}, {self.get_country_display()}, {self.get_region_display()}"


class CoffeeGrind(models.Model):
    grind_id = models.AutoField(primary_key=True)
    grind = models.IntegerField(choices=GRIND_CHOICES)

    def get_grind_display(self):
        return dict(GRIND_CHOICES).get(self.grind)

    def __str__(self):
        return self.get_grind_display()


class CoffeeSize(models.Model):
    size_id = models.AutoField(primary_key=True)
    size = models.DecimalField(null=True, max_digits=10, decimal_places=0)
    unit = models.TextField()

    def __str__(self):
        return f"{self.size} {self.unit}"


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="products")
    origin_id = models.ForeignKey(CoffeeOrigin, on_delete=models.CASCADE,
                                  null=True,
                                  related_name="products")
    grind_id = models.ForeignKey(CoffeeGrind, on_delete=models.CASCADE,
                                 null=True,
                                 related_name="products")
    size_id = models.ForeignKey(CoffeeSize, on_delete=models.CASCADE,
                                null=True,
                                related_name="products")
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    image = CloudinaryField('image')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
