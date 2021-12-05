from django.db import models

# Create your models here.
class Project(models.Model):
    email = models.EmailField(max_length=254)
    image = models.ImageField(upload_to='pics')
    developerName = models.CharField(max_length = 100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.TextField()

