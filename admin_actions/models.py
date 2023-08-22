from django.db import models
from django.contrib.auth.models import User


class Newsletter(models.Model):

    subject = models.CharField(null=True, max_length=254)
    content = models.TextField(null=True, max_length=254)
    created_on = models.DateTimeField(auto_now_add=True)