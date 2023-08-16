from django.db import models

# Create your models here.

class Newsletter(models.Model):

    subject = models.CharField(null=True, max_length=254)
    content = models.TextField(null=True, max_length=254)
