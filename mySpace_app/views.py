import mimetypes
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import InstPublish, InstTeaches, SecCanRead, StudPartOf, User, Student, Faculty, Dept, Course, Section, Notice, CertReq, SemFee, MessFee, Result, StudTakes
from mySpace_app.file import processCSV, processExcel

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
    print("logout")
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

    faculty = Faculty.objects.get(user=request.user)
    return render(request, 'faculty_templates/faculty_profile.html', {'faculty' : faculty})

def faculty_course_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    teaches = InstTeaches.objects.filter(faculty=user)

    courses = []
    for entry in teaches:
        courses.append(entry.course)

    return render(request, 'faculty_template/faculty_course_home.html', {'courses': courses})

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
        noticeList.append([entry.notice, entry.published_on])

    return render(request, 'faculty_templates/faculty_notice_home.html', {noticeList: noticeList})

def faculty_notice_publish(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Faculty.objects.get(user=request.user)
    if request.method == 'POST':
        notice = Notice(notice_name=request.POSt.get('notice_name'), content=request.POST.get('content'))
        notice.save()
        InstPublish(faculty=user, notice=notice).save()
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

    student = Student.objects.get(user=request.user)
    return render(request, 'student_templates/student_profile.html', {'student' : student})

def student_result_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    result = Result.objects.filter(student=user)
    return render(request, 'student_templates/student_result.html', {'sem': range(1, len(result)+1)})

def student_result(request, username, sem):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    filename = user.roll_no + '.pdf'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + f'\\media\\result\\{user.batch}-Batch\\Sem-{sem}\\' + filename

    if not os.path.exists(filepath):
        return redirect(f'/student/{username}/result/')

    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "inline; filename=%s" % filename
    return response

def student_perf_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    takes = StudTakes.objects.filter(student=user)

    all_course = []
    for entry in takes:
        all_course.append(entry.course)
    return render(request, 'student_templates/student_perf_home.html', {'courses': all_course})

def student_perf(request, username, course_id):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    _course = Course.objects.get(id=course_id)
    course = StudTakes.objects.get(student=user, course=_course)
    contents = {
        'quiz1': course.quiz1_score if course.quiz1_score else '-',
        'quiz2': course.quiz2_score if course.quiz2_score else '-',
        'midterm': course.midterm_score if course.midterm_score else '-',
        'endterm': course.endterm_score if course.endterm_score else '-',
        'assignment': course.assignment_score if course.assignment_score else '-'
    }
    return render(request, 'student_templates/student_perf.html', contents)

def student_notice_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    partOf = StudPartOf.objects.get(student=user)
    canRead = SecCanRead.objects.filter(section=partOf.section)

    all_notice = []
    for entry in canRead:
        all_notice.append(entry.notice)
    return render(request, 'student_templates/student_notice_home.html', {'notices': all_notice})

def student_notice(request, username, notice_id):
    if request.user.is_anonymous: return redirect('/login')

    notice = Notice.objects.get(id=notice_id)
    contents = {
        'name': notice.notice_name,
        'content': notice.content
    }
    return render(request, 'student_templates/student_notice.html', contents)

def student_fee_payment_home(request, username):
    if request.user.is_anonymous: return redirect('/login')

    return render(request, 'student_templates/student_fee_payment_home.html')

def student_fee_payment_mess(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    mess_fee_entries = MessFee.objects.filter(student=user)

    all_entries = []
    total_due = 0
    total_paid = 0
    for entry in mess_fee_entries:
        temp = {
            'month': entry.month,
            'year': entry.year,
            'due': entry.mess_fee,
            'paid': entry.mess_fee_paid if entry.mess_fee_paid else 0
        }
        total_due += entry.mess_fee
        if entry.mess_fee_paid: total_paid += entry.mess_fee_paid
        all_entries.append(temp)

    content = {
        'total_entries': len(all_entries),
        'all_entries': all_entries,
        'total_due': total_due,
        'total_paid': total_paid,
        'remaining': total_due - total_paid
    }
    return render(request, 'student_templates/student_fee_payment_mess.html', content)

def student_fee_payment_tuition(request, username):
    if request.user.is_anonymous: return redirect('/login')

    user = Student.objects.get(user=request.user)
    sem_fee_entries = SemFee.objects.filter(student=user)

    all_entries = []
    tuition_due = 0
    tuition_paid = 0
    hostel_due = 0
    hostel_paid = 0
    for entry in sem_fee_entries:
        temp = {
            'semester': entry.semester,
            'tuition_due': entry.tuition_fee,
            'hostel_due': entry.hostel_fee,
            'tuition_paid': entry.tuition_fee_paid if entry.tuition_fee_paid else 0,
            'hostel_paid': entry.hostel_fee_paid if entry.hostel_fee_paid else 0
        }
        tuition_due += entry.tuition_fee
        hostel_due += entry.hostel_fee
        if entry.tuition_fee_paid: tuition_paid += entry.tuition_fee_paid
        if entry.hostel_fee_paid: hostel_paid += entry.hostel_fee_paid
        all_entries.append(temp)

    content = {
        'total_entries': len(all_entries),
        'all_entries': all_entries,
        'tuition_due': tuition_due,
        'tuition_paid': tuition_paid,
        'tuition_remaining': tuition_due - tuition_paid,
        'hostel_due': hostel_due,
        'hostel_paid': hostel_paid,
        'hostel_remaining': hostel_due - hostel_paid
    }
    return render(request, 'student_templates/student_fee_payment_tuition.html', content)

def student_timetable(request, username):
    return render(request, 'student_templates/student_timetable.html')

def student_timetable_exam(request, username):
    if request.user.is_anonymous: return redirect('/login')

    filename = 'Exam.pdf'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + f'\\media\\timetable\\' + filename

    if not os.path.exists(filepath):
        return redirect(f'/student/{username}/timetable/')

    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "inline; filename=%s" % filename
    return response

def student_timetable_class(request, username):
    if request.user.is_anonymous: return redirect('/login')

    filename = 'Class.pdf'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + f'\\media\\timetable\\' + filename

    if not os.path.exists(filepath):
        return redirect(f'/student/{username}/timetable/')

    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "inline; filename=%s" % filename
    return response