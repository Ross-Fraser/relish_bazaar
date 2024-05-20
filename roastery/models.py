from django.db import models

# Create your models here.
GRIND_CHOICES = (
    (0, "Whole Bean"),
    (1, "Coarse"),
    (2, "Medium"),
    (3, "Fine"),
    (4, "Extra Fine")
)


CONTINENT = (
    (0, "Africa"),
    (1, "Asia"),
    (2, "Americas"),
)


COUNTRY = (
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


REGION = (
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
    continent = models.IntegerField(choices=CONTINENT)
    country = models.IntegerField(choices=COUNTRY)
    region = models.IntegerField(choices=REGION)

    def __int__(self):
        return self.continent
    
    # displays the human-readable name of the origin
    def __str__(self):
        return f"{self.get_continent_display()}, {self.get_country_display()}, {self.get_region_display()}"


class CoffeeGrind(models.Model):
    grind_id = models.AutoField(primary_key=True)
    grind = models.IntegerField(choices=GRIND_CHOICES)

    def __int__(self):
        return self.grind
    
    # displays the human-readable name of the grind
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
                                 related_name="product")
    origin_id = models.ForeignKey(CoffeeOrigin, on_delete=models.CASCADE,
                                  null=True,
                                  related_name="product")
    grind_id = models.ForeignKey(CoffeeGrind, on_delete=models.CASCADE,
                                 null=True,
                                 related_name="product")
    size_id = models.ForeignKey(CoffeeSize, on_delete=models.CASCADE,
                                null=True,
                                related_name="product")
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
