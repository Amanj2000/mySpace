from base64 import urlsafe_b64encode
import mimetypes
import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string

from .models import CourseDetails, Fines, InstOf, InstPublish, InstReq, InstTeaches, Section, SecCanRead, StudPartOf, StudReq, User, Student, Faculty, Course, Notice, CertReq, SemFee, MessFee, Result, StudTakes
from .file import processCSV, processExcel
from .utility import factTeaches, getFaculty

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

	faculty = Faculty.objects.get(user=request.user)
	return render(request, 'faculty_templates/faculty_profile.html', {'faculty' : faculty})

def faculty_course_home(request, username):
	if request.user.is_anonymous: return redirect('/login')

	user = Faculty.objects.get(user=request.user)
	teaches = InstTeaches.objects.filter(faculty=user)

	courses = []
	for entry in teaches:
		courses.append(entry.course)

	return render(request, 'faculty_templates/faculty_course_home.html', {'courses': courses})

def faculty_course(request, username, course_id):
	if request.user.is_anonymous: return redirect('/login')

	_faculty = Faculty.objects.get(user=request.user)
	_course = Course.objects.get(id=course_id)
	_inst_teaches = InstTeaches.objects.get(faculty=_faculty, course=_course)
	if request.method == 'POST':
		course_mat = CourseDetails(inst_teaches= _inst_teaches, details=request.FILES.get('File'))
		course_mat.save()

	material = CourseDetails.objects.filter(inst_teaches=_inst_teaches)
	files = []
	for entry in material:
		files.append(os.path.basename(entry.details.name))
	return render(request, 'faculty_templates/faculty_course.html', {'files': files, 'course_id': course_id})


def show_material(request, username, course_id, filename):
	if request.user.is_anonymous: return redirect('/login')

	if Student.objects.filter(user=request.user).exists():
		faculty_name = getFaculty(request.user, course_id).faculty.user.username
	else:
		faculty_name = username

	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	course_name = Course.objects.get(id=course_id).course_name
	filepath = BASE_DIR + f'/media/course_details/{faculty_name}/{course_name}/' + filename

	if not os.path.exists(filepath):
		if Student.objects.filter(user=request.user).exists():
			return redirect(f'/student/{username}/courses/{course_id}/')
		else:
			return redirect(f'/faculty/{username}/courses/{course_id}/')

	path = open(filepath, 'rb')
	mime_type, _ = mimetypes.guess_type(filepath)
	response = HttpResponse(path, content_type=mime_type)
	response['Content-Disposition'] = "inline; filename=%s" % filename
	return response

def faculty_perf_home(request, username):
	if request.user.is_anonymous: return redirect('/login')

	user = Faculty.objects.get(user=request.user)
	teaches = InstTeaches.objects.filter(faculty=user)

	courses = []
	for entry in teaches:
		courses.append(entry.course)

	return render(request, 'faculty_templates/faculty_perf_home.html', {'courses': courses})

def faculty_perf(request, username, course_id):
	if request.user.is_anonymous: return redirect('/login')

	course, stud_allowed = factTeaches(request.user, course_id)
	if request.method == 'POST':
		#Process File
		file = request.FILES.get('File')
		marks_of = request.POST.get('marks_of')
		data = processCSV(file) if file.name.endswith('.csv') else processExcel(file)

		# File format
		# Roll No. Marks
		error_stud = []
		for i in range(0, len(data)):
			try:
				stud = Student.objects.get(roll_no=int(data[i][0]))
				if(stud.user.id not in stud_allowed):
					# error_stud.append((i+1, data[i][0], data[i][1]))
					continue
				temp = StudTakes.objects.get(student=stud, course=course)
				setattr(temp, marks_of, int(data[i][1]))
				temp.save()
			except Exception as e:
				# error_stud.append((i+1, data[i][0], data[i][1]))
				pass
		# print(error_stud)
		messages.success(request, 'File successfully uploaded')

	marks = {}
	attribute = ['quiz1_score', 'midterm_score', 'quiz2_score', 'endterm_score', 'assignment_score']
	for stud_id in stud_allowed:
		temp = StudTakes.objects.get(student=Student.objects.get(user=User.objects.get(id=stud_id)), course=course)
		marks[temp.student.roll_no] = [getattr(temp, attr) if getattr(temp, attr) else '-' for attr in attribute]
	return render(request, 'faculty_templates/faculty_perf.html', {'course_id': course_id, 'marks': marks})

def faculty_notice_home(request, username):
	if request.user.is_anonymous: return redirect('/login')

	user = Faculty.objects.get(user=request.user)
	published = InstPublish.objects.filter(faculty=user)

	noticeList = []
	for entry in published:
		noticeList.append({'note': entry.notice, 'published' :entry.published_on})

	return render(request, 'faculty_templates/faculty_notice_home.html', {'notices': noticeList})

def faculty_notice_publish(request: HttpRequest, username):
	if request.user.is_anonymous: return redirect('/login')
	user = Faculty.objects.get(user=request.user)
	if request.method == 'POST':
		notice = Notice(notice_name=request.POST.get('notice_name'), content=request.POST.get('content'))
		notice.save()
		InstPublish(faculty=user, notice=notice).save()
		sections = request.POST.getlist('sections')
		for sec in sections:
			SecCanRead(section=Section.objects.get(sec_name=sec), notice=notice).save()
		return redirect(f'/faculty/{username}/notice/{notice.id}/')
	else:
		sections = []
		for entry in InstOf.objects.filter(faculty=user):
			sections.append(entry.section.sec_name)
			print(entry.section.sec_name)
		return render(request, 'faculty_templates/faculty_notice_publish.html', {'sections': sections})

def faculty_notice_edit(request, username, notice_id):
	if request.user.is_anonymous: return redirect('/login')

	user = Faculty.objects.get(user=request.user)
	notice = Notice.objects.get(id=notice_id)
	if request.method == 'POST':
		notice.delete()
		notice = Notice(notice_name=request.POST.get('notice_name'), content=request.POST.get('content'))
		notice.save()
		InstPublish(faculty=user, notice=notice).save()
		sections = request.POST.getlist('sections')
		for sec in sections:
			SecCanRead(section=Section.objects.get(sec_name=sec), notice=notice).save()
		return redirect(f'/faculty/{username}/notice/{notice.id}/')
	else:
		sections = {}
		for entry in InstOf.objects.filter(faculty=user):
			sections[entry.section.sec_name] = 0
		for entry in SecCanRead.objects.filter(notice=notice):
			sections[entry.section.sec_name] = 1
		return render(request, 'faculty_templates/faculty_notice_edit.html', {'notice': notice, 'sections': sections})

def faculty_timetable(request, username):
	return render(request, 'faculty_templates/faculty_timetable.html')



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
	filepath = BASE_DIR + f'/media/result/{user.batch}-Batch/Sem-{sem}/' + filename

	if not os.path.exists(filepath):
		return redirect(f'/student/{username}/result/')

	with open(filepath, 'rb') as path:
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "inline; filename=%s" % filename
		return response

def student_course_home(request, username):
	if request.user.is_anonymous: return redirect('/login')

	user = Student.objects.get(user=request.user)
	takes = StudTakes.objects.filter(student=user)

	all_course = []
	for entry in takes:
		all_course.append(entry.course)
	return render(request, 'student_templates/student_course_home.html', {'courses': all_course})

def student_course(request, username, course_id):
	if request.user.is_anonymous: return redirect('/login')

	_inst_teaches = getFaculty(request.user, course_id)
	material = CourseDetails.objects.filter(inst_teaches=_inst_teaches)
	files = []
	for entry in material:
		files.append(os.path.basename(entry.details.name))
	return render(request, 'student_templates/student_course.html', {'files': files, 'course_id': course_id})

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

def notice_view(request, username, notice_id):
	if request.user.is_anonymous: return redirect('/login')

	notice = Notice.objects.get(id=notice_id)
	contents = {
		'name': notice.notice_name,
		'content': notice.content,
		'published_on': notice.published_on
	}
	if Student.objects.filter(user=request.user).exists():
		return render(request, 'student_templates/notice_view.html', contents)
	else:
		return render(request, 'faculty_templates/notice_view.html', contents)

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
			'due': entry.mess_fee if entry.mess_fee else 0,
			'paid': entry.mess_fee_paid if entry.mess_fee_paid else 0
		}
		if entry.mess_fee: total_due += entry.mess_fee
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
			'tuition_due': entry.tuition_fee if entry.tuition_fee else 0,
			'hostel_due': entry.hostel_fee if entry.hostel_fee else 0,
			'tuition_paid': entry.tuition_fee_paid if entry.tuition_fee_paid else 0,
			'hostel_paid': entry.hostel_fee_paid if entry.hostel_fee_paid else 0
		}
		if entry.tuition_fee: tuition_due += entry.tuition_fee
		if entry.hostel_fee: hostel_due += entry.hostel_fee
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

def student_fee_payment_fine(request, username):
	if request.user.is_anonymous: return redirect('/login')

	user = Student.objects.get(user=request.user)
	fine_entries = Fines.objects.filter(student=user)

	all_entries = []
	total_due = 0
	total_paid = 0
	for entry in fine_entries:
		temp = {
			'due': entry.fine if entry.fine else 0,
			'paid': entry.fine_paid if entry.fine_paid else 0,
			'remark': entry.remark
		}
		if entry.fine: total_due += entry.fine
		if entry.fine_paid: total_paid += entry.fine_paid
		all_entries.append(temp)

	content = {
		'total_entries': len(all_entries),
		'all_entries': all_entries,
		'total_due': total_due,
		'total_paid': total_paid,
		'remaining': total_due - total_paid
	}
	return render(request, 'student_templates/student_fee_payment_fine.html', content)

def timetable(request, username):
	if request.user.is_anonymous: return redirect('/login')

	if Student.objects.filter(user=request.user).exists():
		return render(request, 'student_templates/student_timetable.html')
	else:
		return render(request, 'faculty_templates/faculty_timetable.html')

def timetable_exam(request, username):
	if request.user.is_anonymous: return redirect('/login')

	filename = 'Exam.pdf'
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	filepath = BASE_DIR + f'/media/timetable/' + filename

	if not os.path.exists(filepath):
		if Student.objects.filter(user=request.user).exists():
			return redirect(f'/student/{username}/timetable/')
		else:
			return redirect(f'/faculty/{username}/timetable/')


	path = open(filepath, 'rb')
	mime_type, _ = mimetypes.guess_type(filepath)
	response = HttpResponse(path, content_type=mime_type)
	response['Content-Disposition'] = "inline; filename=%s" % filename
	return response

def timetable_class(request, username):
	if request.user.is_anonymous: return redirect('/login')

	filename = 'Class.pdf'
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	filepath = BASE_DIR + f'/media/timetable/' + filename

	if not os.path.exists(filepath):
		if Student.objects.filter(user=request.user).exists():
			return redirect(f'/student/{username}/timetable/')
		else:
			return redirect(f'/faculty/{username}/timetable/')

	path = open(filepath, 'rb')
	mime_type, _ = mimetypes.guess_type(filepath)
	response = HttpResponse(path, content_type=mime_type)
	response['Content-Disposition'] = "inline; filename=%s" % filename
	return response

def cert_req_home(request, username):
	if request.user.is_anonymous: return redirect('/login')

	if Student.objects.filter(user=request.user).exists():
		user = Student.objects.get(user=request.user)
		Req = StudReq.objects.filter(student=user)
		all_request = []
		for entry in Req:
			all_request.append(entry.cert_req)
		return render(request, 'student_templates/cert_req_home.html', {'requests': all_request})
	else:
		user = Faculty.objects.get(user=request.user)
		Req = InstReq.objects.filter(faculty=user)
		all_request = []
		for entry in Req:
			all_request.append(entry.cert_req)
		return render(request, 'faculty_templates/cert_req_home.html', {'requests': all_request})

def cert_req_new(request, username):
	if request.user.is_anonymous: return redirect('/login')

	if request.method == 'POST':
		cert_req = CertReq(type=request.POST.get('type'), add_info=request.POST.get('additional-info'))
		cert_req.save()
		if Student.objects.filter(user=request.user).exists():
			user = Student.objects.get(user=request.user)
			StudReq(student=user, cert_req=cert_req).save()
			return redirect(f'/student/{username}/cert-req/{cert_req.id}/')
		else:
			user = Faculty.objects.get(user=request.user)
			InstReq(faculty=user, cert_req=cert_req).save()
			return redirect(f'/faculty/{username}/cert-req/{cert_req.id}/')
	else:
		if Student.objects.filter(user=request.user).exists():
			return render(request, 'student_templates/cert_req_new.html')
		else:
			return render(request, 'faculty_templates/cert_req_new.html')

def cert_req_view(request, username, cert_id):
	if request.user.is_anonymous: return redirect('/login')

	cert = CertReq.objects.get(id=cert_id)
	contents = {
		'type': cert.type,
		'add_info': cert.add_info,
		'date': cert.req_date,
		'response': cert.response
	}
	if Student.objects.filter(user=request.user).exists():
		return render(request, 'student_templates/cert_req_view.html', contents)
	else:
		return render(request, 'faculty_templates/cert_req_view.html', contents)



#Forget password view
def password_reset(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(email=data)
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
						'email':user.email,
						'domain':'127.0.0.1:8000',
						'site_name': 'mySpace',
						'uid': urlsafe_b64encode(force_bytes(user.pk)).decode(),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'mySpace.Web@outlook.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request, "password_reset.html", context={"password_reset_form":password_reset_form})