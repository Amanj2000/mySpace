from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    dob = models.DateField(default = datetime.date(1950, 1, 1))

    gender_choices = [('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Others')]
    gender = models.CharField(default = 'O', max_length=1, choices= gender_choices)
    phone = models.CharField(max_length=10)
    roll_no = models.CharField(max_length = 7)
    batch = models.PositiveSmallIntegerField(default = datetime.datetime.now().year)

class Faculty(models.Model):
    class Meta:
        verbose_name_plural = "Faculties"
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    dob = models.DateField(default = datetime.date(1950, 1, 1))

    gender_choices = [('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Others')]
    gender = models.CharField(default = 'O', max_length=1, choices= gender_choices)
    phone = models.CharField(max_length=10)
    rank = models.PositiveSmallIntegerField(default = 100)
    research_area = models.CharField(default= 'Technology', max_length=20)