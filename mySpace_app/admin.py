from django.contrib import admin
from .models import Student, Faculty, Dept, Course, Section, Notice, CertReq, SemFee, MessFee, Result, StudTakes

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Dept)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Notice)
admin.site.register(CertReq)
admin.site.register(SemFee)
admin.site.register(MessFee)
admin.site.register(Result)
admin.site.register(StudTakes)

# Change header
admin.site.site_header = "mySpace administration"
