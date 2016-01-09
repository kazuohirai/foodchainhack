from django.db import models

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        x = 'Name: ' + self.name + '\n' + 'Address: ' + self.address
        return x
