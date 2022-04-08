from django.contrib import admin
from .models import Student, Faculty, Dept, Course, Section, Tag, Notice, NoticeTag, CertReq, SemFee, MessFee, Result, InstTeaches, \
                    StudTakes, InstOf, StudPartOf, InstReq, StudReq, AdminReview, AdminPublish, InstPublish, SecCanRead, TimeTable

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Dept)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Tag)
admin.site.register(Notice)
admin.site.register(NoticeTag)
admin.site.register(CertReq)
admin.site.register(SemFee)
admin.site.register(MessFee)
admin.site.register(Result)
admin.site.register(InstTeaches)
admin.site.register(StudTakes)
admin.site.register(InstOf)
admin.site.register(StudPartOf)
admin.site.register(InstReq)
admin.site.register(StudReq)
admin.site.register(AdminReview)
admin.site.register(AdminPublish)
admin.site.register(InstPublish)
admin.site.register(SecCanRead)
admin.site.register(TimeTable)


# Change header
admin.site.site_header = "mySpace administration"
