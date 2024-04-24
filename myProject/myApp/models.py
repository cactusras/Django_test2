from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=50)
class Person(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)