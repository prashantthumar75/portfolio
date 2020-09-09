from django.db import models

# Create your models here.

class ContactModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    number = models.IntegerField()
    message = models.TextField(max_length=1500)