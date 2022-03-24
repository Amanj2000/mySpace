from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Dept(models.Model):
    dept_name = models.CharField(max_length=50)

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


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    dob = models.DateField(default = datetime.date(1950, 1, 1))

    gender_choices = [('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Others')]
    gender = models.CharField(default = 'O', max_length=1, choices= gender_choices)
    phone = models.CharField(max_length=10)
    designation = models.CharField(max_length=20)

class Course(models.Model):
    course_name = models.CharField(max_length=40)
    grade = models.PositiveSmallIntegerField()
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)

class Section(models.Model):
    sec_name = models.CharField(max_length=10)

class Tag(models.Model):
    tag_name = models.CharField(max_length=10)

class Notice(models.Model):
    notice_name = models.CharField(max_length=255)
    content = models.TextField()

class Notice_Tag(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Cert_Req(models.Model):
    type = models.CharField(max_length=20)
    add_info = models.TextField()

    response_type = models.TextChoices('Response', 'Approved Denied Pending')
    response = models.CharField(choices=response_type.choices, max_length=10)

class Sem_Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    tuition_fee = models.IntegerField(blank=True)
    hostel_fee = models.IntegerField(blank=True)
    
    class Meta:
        unique_together = (('student', 'semester'), )

class Mess_Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    mess_fee = models.IntegerField(blank=True)
    
    class Meta:
        unique_together = (('student', 'month', 'year'), )

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    result = models.FileField()
    
    class Meta:
        unique_together = (('student', 'semester'), )

class Inst_Teaches(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Stud_Takes(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz1_score = models.IntegerField(null=True)
    quiz2_score = models.IntegerField(null=True)
    midterm_score = models.IntegerField(null=True)
    endterm_score = models.IntegerField(null=True)
    assignment_score = models.IntegerField(null=True)


class Inst_Of(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Stud_Part_Of(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Inst_Req(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(Cert_Req, on_delete=models.CASCADE)
    req_date = models.DateTimeField(default=datetime.datetime.now())

class Stud_Req(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(Cert_Req, on_delete=models.CASCADE)
    req_date = models.DateTimeField(default=datetime.datetime.now())

class Admin_Review(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    cert_req = models.ForeignKey(Cert_Req, on_delete=models.CASCADE)
    review_date = models.DateTimeField(default=datetime.datetime.now())

class Admin_Publish(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    published_on = models.DateTimeField(default=datetime.datetime.now())
    
class Inst_Publish(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    published_on = models.DateTimeField(default=datetime.datetime.now())

class Sec_Can_Read(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
