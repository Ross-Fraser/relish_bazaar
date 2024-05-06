from django.db import models

# Create your models here.
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name