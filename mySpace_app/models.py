from django.db import models

# Create your models here.
class Dept(models.Model):
    id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=255)