import mimetypes
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import SecCanRead, StudPartOf, User, Student, Faculty, Dept, Course, Section, Notice, CertReq, SemFee, MessFee, Result, StudTakes

# Create your views here.
def home(request):
    if request.user.is_anonymous:
        return redirect("/login") 
    elif request.user.is_superuser:
        return redirect('/admin')
    elif Student.objects.filter(user=request.user).exists():
        return redirect('/student')
    else:
        return redirect('/faculty')

def loginUser(request):
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            elif Student.objects.filter(user=request.user).exists():
                return redirect('/student')
            else:
                return redirect('/faculty')
        else:
            messages.error(request,"Invalid Login Credentials")
    return render(request,"login_page.html")

def logoutUser(request):
    logout(request)
    return redirect('/login')

#Faculty views

def faculty_home(request):
    user_obj=User.objects.get(id=request.user.id)
    return render(request,"faculty_templates/faculty_home.html",{"name":user_obj.first_name})

#Student views

def student(request):
    if request.user.is_anonymous: return redirect('/login')

    print(request.user)
    return redirect(f'/student/{request.user.username}')
    
def student_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = User.objects.get(username=username)
    return render(request,"student_templates/student_home.html",{"name":user})

def student_profile(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = User.objects.get(username=username)
    contents = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'dob': user.dob,
        'gender': user.gender,
        'phone': user.phone,
        'roll_no': user.roll_no,
        'batch': user.batch,
        'dept': user.dept
    }
    return render(request, 'student_templates/student_profile.html', contents)

def student_result_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = User.objects.get(username=username)
    result = Result.objects.filter(student=user.id)
    return render(request, 'student_templates/student_result.html', len(result))

def student_result(request, username, sem):
    if request.user.is_anonymous: return redirect('/login')

    # to-do: check if file exists
    user = User.objects.get(username=username)
    filename = user.roll_no + sem + '.pdf'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + '/media/' + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
    
def student_perf_home(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    course = StudTakes.objects.filter(student=user.id)
    return render(request, 'student_templates/student_perf_home.html', len(course))

def student_perf(request, username, course_id):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    course = StudTakes.objects.filter(student=user.id, course=course_id)
    contents = {
        'quiz1': course.quiz1_score, 
        'quiz2': course.quiz2_score, 
        'midterm': course.midterm_score, 
        'endterm': course.endterm_score, 
        'assignment': course.assignment_score, 
    }
    return render(request, 'student_templates/student_perf.html', contents)

def student_notice_home(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    partOf = StudPartOf.objects.get(student=user.id)
    canRead = SecCanRead.objects.filter(section=partOf.section)

    all_notice = []
    for notice in canRead:
        all_notice.append(Notice.objects.get(id=notice.notice))
    return render(request, 'student_templates/student_notice_home.html', all_notice)

def student_notice(request, username, notice_id):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    partOf = StudPartOf.objects.get(student=user.id)
    notice = SecCanRead.objects.filter(section=partOf.section, notice=notice_id)
    
    contents = {
        'name': notice.notice_name,
        'content': notice.notice_content
    }
    return render(request, 'student_templates/student_notice_home.html', contents)
    
def student_fee_payment_home(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    return render(request, 'student_templates/student_fee_payment_home')

def student_fee_payment_mess(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    mess_fee_entries = MessFee.objects.filter(student=user.id)

    return render(request, 'student_templates/student_fee_payment_mess', mess_fee_entries)

def student_fee_payment_tuition(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = User.objects.get(username=username)
    sem_fee_entries = SemFee.objects.filter(student=user.id)

    return render(request, 'student_templates/student_fee_payment_tuition', sem_fee_entries)
