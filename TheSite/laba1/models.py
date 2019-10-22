from django.db import models

class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    soname = models.CharField(max_length=30)
    patonymic = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    