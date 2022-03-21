from django.contrib import admin
from .models import Student, Faculty

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)

# Change header
admin.site.site_header = "mySpace administration"
