from django.db import models

class Status(models.TextChoices):
    A = ('A', 'A')
    B = ('B', 'B')
    C = ('C', 'C')


class Gender(models.Model):
    designation = models.TextField(null=False)
    creator = models.CharField(max_length=255, blank=False)
    create_date = models.DateTimeField(blank=False)
    modifier = models.CharField(max_length=255, blank=False)
    modified_date = models.DateTimeField(blank=False)


class Person(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    height = models.IntegerField(null=False)
    birth_date = models.DateField(null=False)
    state = models.CharField(max_length=1, choices=Status.choices, null=False)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, null=True)
    creator = models.CharField(max_length=255, blank=False)
    create_date = models.DateTimeField(blank=False)
    modifier = models.CharField(max_length=255, blank=False)
    modified_date = models.DateTimeField(blank=False)


