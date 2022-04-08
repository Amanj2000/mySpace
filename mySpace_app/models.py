from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mySpace_app.storage import OverwriteStorage
import datetime

# Create your models here.

class Dept(models.Model):
    dept_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.dept_name

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
    dept = models.ForeignKey(Dept, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

    def clean(self):
        if Faculty.objects.filter(user=self.user).exists():
             raise ValidationError({'user': ['User is already registered as a faculty.']})

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
    rank = models.CharField(max_length=20)
    research_area = models.CharField(default= 'Technology', max_length=20)
    dept = models.ForeignKey(Dept, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username
    
    def clean(self):
        if Student.objects.filter(user=self.user).exists():
            raise ValidationError({'user': ['User is already registered as a student.']})

class Course(models.Model):
    course_name = models.CharField(max_length=40, unique=True)
    grade = models.PositiveSmallIntegerField()
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

class Section(models.Model):
    sec_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.sec_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.tag_name

class Notice(models.Model):
    notice_name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.notice_name

class NoticeTag(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('notice', 'tag'), )

    def __str__(self):
        return self.notice.notice_name + '_' + self.tag.tag_name

class CertReq(models.Model):
    type = models.CharField(max_length=20)
    add_info = models.TextField()

    response_type = models.TextChoices('Response', 'Approved Denied Pending')
    response = models.CharField(choices=response_type.choices, max_length=10)

class SemFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    tuition_fee = models.IntegerField()
    hostel_fee = models.IntegerField()
    tuition_fee_paid = models.IntegerField(null=True, blank=True)
    hostel_fee_paid = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('student', 'semester'), )

    def __str__(self):
        return self.student.user.username + '_' + str(self.semester)

class MessFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    mess_fee = models.IntegerField()
    mess_fee_paid = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('student', 'month', 'year'), )
    
    def __str__(self):
        return self.student.user.username + '_' + str(self.month) + '_' + str(self.year)

class Result(models.Model):
    def semwise_upload_to(self, filename):        
        return f'media/result/{self.student.batch}-Batch/Sem-{self.semester}/{self.student.roll_no}.pdf'

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    result = models.FileField(max_length=30, upload_to=semwise_upload_to, storage=OverwriteStorage())

    class Meta:
        unique_together = (('student', 'semester'), )
    
    def __str__(self):
        return self.student.user.username + '_' + str(self.semester)

class InstTeaches(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('faculty', 'course'), )

    def __str__(self):
        return self.faculty.user.username + '_' + self.course.course_name

class StudTakes(models.Model):
    class Meta:
        verbose_name_plural = "Students Takes"
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz1_score = models.IntegerField(null=True, blank=True)
    quiz2_score = models.IntegerField(null=True, blank=True)
    midterm_score = models.IntegerField(null=True, blank=True)
    endterm_score = models.IntegerField(null=True, blank=True)
    assignment_score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('student', 'course'), )

    def __str__(self):
        return self.student.user.username + '_' + self.course.course_name


class InstOf(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('faculty', 'section'), )

    def __str__(self):
        return self.faculty.user.username + '_' + self.section.sec_name

class StudPartOf(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'section'), )

    def __str__(self):
        return self.student.user.username + '_' + self.section.sec_name

class InstReq(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(CertReq, on_delete=models.CASCADE)
    req_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('faculty', 'cert_req'), )

    def __str__(self):
        return self.faculty.user.username + '_' + self.cert_req.id

class StudReq(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(CertReq, on_delete=models.CASCADE)
    req_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('student', 'cert_req'), )
    
    def __str__(self):
        return self.student.user.username + '_' + self.cert_req.id

class AdminReview(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(CertReq, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('admin', 'cert_req'), )

    def __str__(self):
        return self.admin.username + '_' + self.cert_req.id

class AdminPublish(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('admin', 'notice'), )
    
    def __str__(self):
        return self.admin.username + '_' + self.notice.notice_name

class InstPublish(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('faculty', 'notice'), )
    
    def __str__(self):
        return self.faculty.user.username + '_' + self.notice.notice_name

class SecCanRead(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)

    def __str__(self):
        return self.section.sec_name + '_' + self.notice.notice_name

    class Meta:
        unique_together = (('section', 'notice'), )

class TimeTable(models.Model):
    def type_upload_to(self, filename):        
        return f'media/timetable/{self.type}.pdf'

    type_choices = [('Class', 'Class TimeTable'),
                    ('Exam', 'Exam TimeTable')]
    type = models.CharField(default = 'Class', max_length=5, choices= type_choices, unique=True)
    schedule = models.FileField(max_length=30, upload_to=type_upload_to, storage=OverwriteStorage())

    def __str__(self):
        return self.type