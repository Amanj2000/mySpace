from http.client import HTTPResponse
import mimetypes
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import InstPublish, InstTeaches, SecCanRead, StudPartOf, User, Student, Faculty, Dept, Course, Section, Notice, CertReq, SemFee, MessFee, Result, StudTakes

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
            return redirect('/')
        else:
            messages.error(request,"Invalid Login Credentials")
    return render(request,"login_page.html")

def logoutUser(request):
    logout(request)
    return redirect('/login')

#Faculty views

def faculty(request):
    if request.user.is_anonymous: return redirect('/login')

    return redirect(f'/faculty/{request.user.username}')

def faculty_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    return render(request,"faculty_templates/faculty_home.html",{"name":user})

def faculty_profile(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    contents = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'dob': user.dob,
        'gender': user.gender,
        'phone': user.phone,
        'rank': user.rank,
        'research_area': user.research_area,
        'dept': user.dept
    }
    return render(request, 'faculty_templates/faculty_profile.html', contents)

def faculty_course_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    teaches = InstTeaches.objects.filter(faculty=user)

    course_name = []
    for entry in teaches:
        course_name.append(Course.objects.get(id=entry.course).course_name)
    
    return render(request, 'faculty_template/faculty_course_home.html', course_name)

def faculty_course_perf(request, username, course_id):
    if request.user.is_anonymous: return redirect('/login')

    #to-do: a way for faculty to upload perf of student for each course
    return HttpResponse('Page In Progress')

def faculty_notice_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    published = InstPublish.objects.get(faculty=user)

    noticeList = []
    for entry in published:
        noticeList.append([Notice.objects.get(id=entry.notice), entry.published_on])
    
    return render(request, 'faculty_templates/faculty_notice_home.html', noticeList)

def faculty_notice_publish(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = Faculty.objects.get(user=request.user)
    if request.method == 'POST':
        notice = Notice(notice_name=request.POSt.get('notice_name'), content=request.POST.get('content'))
        notice.save()
        InstPublish(faculty=user.id, notice=notice.id).save()
        return redirect(f'/faculty/{username}/notice')
    else:
        return render(request, 'faculty_templates/faculty_notice_publish.html')

def faculty_notice_edit(request, username, notice_id):
    if request.user.is_anonymous: return redirect('/login')
    
    if request.method == 'POST':
        notice = Notice.objects.get(id=notice_id)
        notice.notice_name = request.POSt.get('notice_name')
        notice.content = request.POST.get('content')
        notice.save()
        return redirect(f'/faculty/{username}/notice')
    else:
        return render(request, 'faculty_templates/faculty_notice_publish.html')
    


#Student views

def student(request):
    if request.user.is_anonymous: return redirect('/login')

    return redirect(f'/student/{request.user.username}')
    
def student_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    return render(request,"student_templates/student_home.html",{"name":user})

def student_profile(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
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

    user = Student.objects.get(user=request.user)
    result = Result.objects.filter(student=user.id)
    return render(request, 'student_templates/student_result.html', len(result))

def student_result(request, username, sem):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    filename = user.roll_no + '_' + str(sem) + '.pdf'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + '/media/' + filename

    if not os.path.exists(filepath):
        return redirect(f'student/{username}/result')

    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
    
def student_perf_home(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = Student.objects.get(user=request.user)
    takes = StudTakes.objects.filter(student=user.id)

    course_name = []
    for entry in takes:
        course_name.append(Course.objects.get(id=entry.course).name)
    return render(request, 'student_templates/student_perf_home.html', course_name)

def student_perf(request, username, course_id):
    if request.user.is_anonymous: return redirect('/login')
    
    user = Student.objects.get(user=request.user)
    course = StudTakes.objects.get(student=user.id, course=course_id)
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
    
    user = Student.objects.get(user=request.user)
    partOf = StudPartOf.objects.get(student=user.id)
    canRead = SecCanRead.objects.filter(section=partOf.section)

    all_notice = []
    for entry in canRead:
        all_notice.append(Notice.objects.get(id=entry.notice))
    return render(request, 'student_templates/student_notice_home.html', all_notice)

def student_notice(request, username, notice_id):
    if request.user.is_anonymous: return redirect('/login')
    
    user = Student.objects.get(user=request.user)
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
    
    user = Student.objects.get(user=request.user)
    mess_fee_entries = MessFee.objects.filter(student=user.id)

    return render(request, 'student_templates/student_fee_payment_mess', mess_fee_entries)

def student_fee_payment_tuition(request, username):
    if request.user.is_anonymous: return redirect('/login')
    
    user = Student.objects.get(user=request.user)
    sem_fee_entries = SemFee.objects.filter(student=user.id)

    return render(request, 'student_templates/student_fee_payment_tuition', sem_fee_entries)
