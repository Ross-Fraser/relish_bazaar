from django.db import models

# Create your models here.
class Categorie(models.Model):
    category_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    sub_category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name