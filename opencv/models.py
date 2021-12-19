from django.db import models

# Create your models here.


class MyModel(models.Model):
    time=models.CharField(max_length=50)
    people_count=models.IntegerField()
    