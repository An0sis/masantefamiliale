from django.db import models
from django.contrib.auth.models import User
import json


class Disease(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField(default='2000-01-01')
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    brother_sister = models.TextField(default='[]', blank=True, null=True)
    gender = models.BooleanField(default=True)
    diseases = models.ManyToManyField(Disease, blank=True)
    
    def __str__(self):
        return self.name + " - " + self.lastname

    def get_brother_sister(self):
        return json.loads(self.brother_sister)

    def set_brother_sister(self, value):
        self.brother_sister = json.dumps(value)

